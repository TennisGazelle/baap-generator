from flask import Flask, request, send_file
import yamale
import json
import os
import sys
import requests
import zipfile
from pathlib import Path

VERSION = "0.0.1"
SCHEMA_FILE='../blender-pipeline/scripts/config_schema.yaml'
schema = yamale.make_schema(SCHEMA_FILE)
tempdir = 'tempdir/'

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "."

@app.route("/", methods=["GET"])
def home():
    return "<h1>Hi there!!!</h1>"


def save_file_and_validate(uploaded_file, path):
    filename = path + "/" + uploaded_file.filename
    uploaded_file.save(filename)

    uploaded_yamale = yamale.make_data(filename)

    return uploaded_yamale


def generate_makefile(stages, models, makefileName):
    makefile_contents = [
        "#",
        "#",
        "# Makefile Generated by validator.py (tennisgazelle)",
        "#",
        "#",
        ""
    ]

    render_contents = []
    get_paths_contents = set()
    set_paths_contents = set()
    all_recipe_names = []

    for stage in stages:
        recipe_name = stage + '_render'
        blend_file = stages[stage]['blend_file']

        all_recipe_names.append(recipe_name)
        render_contents.append(f'{recipe_name}: blender/{blend_file}')
        render_contents.append(f'\tpython3 scripts/render.py --stage {stage}')
        render_contents.append('')
        get_paths_contents.add(f'\tdocker run --rm -v ${{PWD}}/blender/:/blender/ -v ${{PWD}}/scripts:/scripts -v ${{PWD}}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/{blend_file} --python scripts/get_path.py')
        set_paths_contents.add(f'\tdocker run --rm -v ${{PWD}}/blender/:/blender/ -v ${{PWD}}/scripts:/scripts -v ${{PWD}}/config.yaml:/config.yaml tennisgazelle/blender-pipeline:latest blender/{blend_file} --python scripts/set_path.py')

    makefile_contents = makefile_contents + \
            ["all: " + " ".join(all_recipe_names)] + [""] + \
            render_contents + \
            ["get_paths:"] + list(get_paths_contents) + [""] + \
            ["set_paths:"] + list(set_paths_contents) + [""] + [
                "clean:",
                "\trm -rf out/",
                "",
                "clean_buffers:",
                "\trm -rf buffer/"
            ]

    with open(makefileName, 'w+') as mfhandle:
        mfhandle.writelines("%s\n" % line for line in makefile_contents)

@app.route("/generate", methods=["POST"])
def generateRelease():

    r = requests.get("https://github.com/TennisGazelle/blender-pipeline/archive/refs/tags/v0.0.1.zip")
    open('baap-template.zip', 'wb').write(r.content)
    

    with zipfile.ZipFile('baap-template.zip', 'r') as zip_file:
        zip_file.extractall(tempdir)
        blender_pipeline_dir = "blender-pipeline-" + VERSION + "/"

    if request.files:

        uploaded_config = request.files.getlist('payload')[0]
        configFile = uploaded_config.filename
        
        try:
            uploaded_yamale = save_file_and_validate(uploaded_config, tempdir)[0][0]
        except Exception as err:
            return {
                "error": "Bad yaml",
                "msg": str(err)
            }

        print('===> generating for config...', uploaded_yamale)
        generate_makefile(uploaded_yamale['stages'], uploaded_yamale['models'], tempdir + blender_pipeline_dir + 'Makefile')

        print('====> copying config...')
        os.rename(tempdir + configFile, tempdir + blender_pipeline_dir + "config.yaml")


        print('zipping....')
        with zipfile.ZipFile('baap-template.zip', 'w') as myzip:
            myzip.write(tempdir + blender_pipeline_dir)
            for dirname, subdirs, files in os.walk(tempdir + blender_pipeline_dir):
                myzip.write(dirname)

                for filename in files:
                    myzip.write(os.path.join(dirname, filename))

            myzip.close()


    return send_file('baap-template.zip')

@app.route("/validate", methods=["POST"])
def validateAgainstSchema():
    data = {}

    if request.files:
        for uploaded_file in request.files.getlist('payload'):
            if uploaded_file.filename != '':
                data[uploaded_file.filename] = {}
                try:
                    uploaded_yamale = save_file_and_validate(uploaded_file, ".")
                    data[uploaded_file.filename] = {
                        "error": None
                    }
                except Exception as err:
                    data[uploaded_file.filename] = {
                        "error": "Malformed yaml",
                        "msg": str(err)
                    }

    else:
        data = request.get_json(force=True)


    return {
        "request": data
    }


app.run()



# # CONFIG_FILE='./config.yaml'


# def init_config():
#     # validate the yaml first
#     import yamale
#     schema = yamale.make_schema(SCHEMA_FILE)
#     # Create a Data object
#     data = yamale.make_data(CONFIG_FILE)
#     # Validate data against the schema. Throws a ValueError if data is invalid.
#     yamale.validate(schema, data)

#     # return it if it works
#     with open('config.yaml', 'r') as config_file:
#         config = yaml.load(config_file)#, Loader=yaml.FullLoader) # fix this