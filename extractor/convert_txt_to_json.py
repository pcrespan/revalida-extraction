import json
import re

def processar_arquivo_texto(nome_arquivo):
    questoes = []
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        with open('answers/extracted/2011.txt', 'r', encoding='utf-8') as txt:
            respostas = {}
            questao = {}
            alternativas = {}

            for linha in txt:
                linha = linha.strip()
                if re.match(r"^\d+\s+[A-E|X]$", linha):
                    numero, resposta = linha.split()
                    respostas[numero] = resposta

            for linha in file:
                linha = linha.strip()

                if linha.startswith("QUESTÃO") or linha.startswith("Questão") or linha.startswith("questão"):
                    if questao:
                        questao['alternativas'] = alternativas
                        questoes.append(questao)
                        questao = {}
                        alternativas = {}
                    numero_questao = int(linha.split()[1])
                    questao['numero'] = numero_questao

                elif linha and (linha[0] in "ABCDE"):
                    letra, texto_alternativa = linha[0], linha[2:].strip()
                    alternativas[letra] = texto_alternativa

                elif linha:
                    if 'enunciado' not in questao:
                        questao['enunciado'] = linha
                    else:
                        questao['enunciado'] += " " + linha
                questao['resposta'] = respostas[str(questao['numero'])]
            if questao:
                questao['alternativas'] = alternativas
                questoes.append(questao)

    return questoes


def salvar_json(questoes, nome_arquivo_json):
    with open(nome_arquivo_json, 'w', encoding='utf-8') as file:
        json.dump({"questoes": questoes}, file, ensure_ascii=False, indent=4)

#tests = [2011, 2012, 2013, 2014, 2015, 2016]
tests = [2011]

for test in tests:
    arquivo_texto = "tests/{}.txt".format(test)
    arquivo_json = "questoes{}.json".format(test)
    questoes_processadas = processar_arquivo_texto(arquivo_texto)
    salvar_json(questoes_processadas, arquivo_json)
    print(f"Questões processadas e salvas em {arquivo_json}")