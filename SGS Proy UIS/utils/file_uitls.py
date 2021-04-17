import marshmallow_dataclass
import re
from models.instance import Instance
from models.pascal_scheme import PascalScheme
import json

baseFilePath = "D:\VS\Proyecto SGS UIS\SGS Proy UIS"

def get_instance_from_file(fileName):
    print('\nReading Json file...')      
    instance_schema = marshmallow_dataclass.class_schema(Instance, base_schema=PascalScheme)()

    with open(f'{baseFilePath}\Resources\instance{fileName}.json', 'r', encoding='utf-8', errors='ignore') as j:
        json_dic = json.loads(j.read())
    return instance_schema.load(json_dic)


def load_results(fileName):
    with open(f'{baseFilePath}\Results\Linea Base Asc {fileName}.lst', 'r', encoding='utf-8', errors='ignore') as j:
        data = j.read()

        result = (re.search('periodo de inicio real transformado', data))
        index1 = result.end()
        index2 = data.rfind('EXECUTION TIME')

        filtered = data[index1: index2]

        print(filtered)

        result = filtered.replace(',', '').split('\n')
        result = [line for line in result if line != '' and line != '\n']
        results = []
        for line in result:
            fields = line.split(' ')
            fields = [l for l in fields if l != '']

            for i in range(0, len(fields), 2):
                tup1 = fields[i].replace('\n', '')
                tup2 = fields[i+1].replace('\n', '')
                results.append([int(tup1.strip()), float(tup2.strip())])
        return results
        