import re
import json

tests = [2011, 2012, 2013, 2014, 2015, 2016]

def extract_answers(path):
    answers = {}

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    answer_regex = re.compile(r"(\d+)\s([A-EX])")

    for match in re.finditer(answer_regex, content):
        numero = int(match.group(1))
        resposta = match.group(2)
        answers[numero] = resposta

    return answers

def contains_img(path):

    img_presence = {}

    with open(path, "r", encoding="utf-8") as file:

        for line in file:
            line = line.strip()
            if line.isdigit():
                img_presence[int(line)] = True

    return img_presence

def convert_to_json(path, test):

    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    questao_regex = r"QUESTÃO (\d+)\n(.*?)\n([A-E] .+?)(?=\nQUESTÃO|\Z)"
    alternativa_regex = r"([A-E]) (.+?)(?=(?:\n[A-E] |\Z))"

    questoes = []
    respostas = extract_answers("answers/extracted/{}.txt".format(test))
    imgs = contains_img("images/{}.txt".format(test))

    for match in re.finditer(questao_regex, content, re.DOTALL):
        numero = int(match.group(1))
        enunciado = match.group(2).strip()
        alternativas_text = match.group(3).strip()

        alternativas = {}
        for alt_match in re.finditer(alternativa_regex, alternativas_text, re.DOTALL):
            letra = alt_match.group(1)
            texto = alt_match.group(2).strip()
            alternativas[letra] = texto

        questao = {
            "numero": numero,
            "enunciado": enunciado,
            "alternativas": alternativas
        }
        questao["resposta"] = respostas[questao["numero"]]

        if imgs.get(questao["numero"]):
            questao["contains_img"] = True
        else:
            questao["contains_img"] = False

        questoes.append(questao)

    json_output = json.dumps(questoes, ensure_ascii=False, indent=4)
    save_json(json_output, test)


def save_json(output, test):
    output_path = "json/questoes{}.json".format(test)
    with open(output_path, "w", encoding="utf-8") as json_file:
        json_file.write(output)
    print(f"JSON gerado e salvo em {output_path}")

for test in tests:
    path = "tests/{}.txt".format(test)
    convert_to_json(path, test)