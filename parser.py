import xmltodict, json
import os
import click
import pandas as pd

swc_filename = 'aligned.swc'

@click.command()
@click.option("--files_directory", '-fd')
def main(files_directory):
    parse_files(files_directory)


def df_ize(doc_as_array, address):
    df = pd.DataFrame(
        doc_as_array,
        columns=["term", "start_time", "end_time", "phonemes"]
    )
    df.to_csv(address, sep="\t", encoding='utf-8')


def parse_files(swc_loc):
    """
    This loads in *all* the text files and writes out the jsons
    It also returns content, the dictionaries representing each xml file
    :param swc_loc:
    :return: files_, a simplified dict format of the xml
    """
    for root, dirs, files in os.walk(swc_loc):
        if swc_filename in files:
            parse_file(root, swc_filename)


def parse_file(root, swc_filename):
    file_loc = root + '/' + swc_filename
    file_str = open(file_loc).read()
    file_dict = xmltodict.parse(file_str)
    file_json = json.dumps(file_dict)
    with open(root + '/' + swc_filename + '.json', 'w') as fid:
        fid.write(file_json + '\n')
    file_dict = json.loads(file_json)
    df_filename = root + '/' + swc_filename + '.df'
    try:
        df_ize(parse_document(file_dict), df_filename)
    except KeyError:
        print "Could not create", df_filename


def parse_metadata(file_dict):
    link = file_dict['article']['meta']['link']
    for meta in link:
        if meta['@key']=='DC.source.text':
            text = meta['@value']
        if meta['@key']=='DC.source.audio':
            sound_file = meta['@value']
    try:
        return text, sound_file
    except:
        return None


def printer(pt_n):
    if '@start' in pt_n:
        start = pt_n['@start']
    else:
        start = 0
    if '@end' in pt_n:
        end = pt_n['@end']
    else:
        end = 0
    if 'ph' in pt_n:
        phon = pt_n['ph']
    else:
        phon = 'NA'
    if '@pronunciation' in pt_n:
        pronun = pt_n['@pronunciation']
    else:
        pronun = ''
    return [pronun, start, end, phon]


def parse_document(file_dict):
    document = file_dict['article']['d']['p']
    morphemes = []
    for utterance in document:
        if type(utterance)==dict and 's' in utterance:
            for word in utterance['s']:
                if type(word)==dict:
                    data = word['t']
                    if type(data)==list:
                        for obs in data:
                            if type(obs)==dict and 'n' in obs:
                                pts = obs['n']
                                if type(pts)==dict:
                                    morphemes.append(printer(pts))
                                elif type(pts)==list:
                                    for item in pts:
                                        morphemes.append(printer(item))
                                else:
                                    morphemes.append([pts, 0, 0, 'NA'])
                            else:
                                morphemes.append([obs, 0, 0, 'NA'])
    return morphemes


if __name__=="__main__":
    main()