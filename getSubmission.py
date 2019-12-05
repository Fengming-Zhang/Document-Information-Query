import csv


def loadAnswer():
    title_answer_num = 0
    with open('title_data/title_submission.csv', 'r', encoding='UTF-8') as titlefile:
        reader = csv.reader(titlefile)
        for line in reader:
            title_answer_num += 1
            if title_answer_num == 1:
                continue
            if line[0] not in query_id:
                query_id.append(line[0])
            if line[0] in title_answer:
                title_answer[line[0]].append(line[1])
            else:
                title_answer[line[0]] = [line[1]]

            if line[0] in title_answer_sim:
                title_answer_sim[line[0]][line[1]] = float(line[2])
            else:
                title_answer_sim[line[0]] = {}
                title_answer_sim[line[0]][line[1]] = float(line[2])

    doc_num = 0
    with open('doc_data/doc_submission.csv', 'r', encoding='UTF-8') as docfile:
        reader = csv.reader(docfile)
        for line in reader:
            doc_num += 1
            if doc_num == 1:
                continue
            if line[0] in doc_answer:
                doc_answer[line[0]].append(line[1])
            else:
                doc_answer[line[0]] = [line[1]]
            if line[0] in doc_answer_sim:
                doc_answer_sim[line[0]][line[1]] = float(line[2])
            else:
                doc_answer_sim[line[0]] = {}
                doc_answer_sim[line[0]][line[1]] = float(line[2])

    print('Load answer done!')


def getMixedSim():
    for query in query_id:
        MixedSim[query] = {}
        for doc in title_answer[query]:
            MixedSim[query][doc] = title_answer_sim[query][doc]
        for doc in doc_answer[query]:
            if doc in MixedSim[query]:
                MixedSim[query][doc] += doc_answer_sim[query][doc]
            else:
                MixedSim[query][doc] = doc_answer_sim[query][doc]


def outputSubmission():
    with open('submissions/submission.csv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["query_id", "doc_id"])
        print(len(query_id))
        for query in query_id:
            answer_num = 0
            for doc in sorted(MixedSim[query], key=MixedSim[query].__getitem__, reverse=True):
                answer_num += 1
                write_temp = [query, doc]
                if doc in title_answer_sim[query]:
                    write_temp.append(title_answer_sim[query][doc])
                else:
                    write_temp.append(0.)
                if doc in doc_answer_sim[query]:
                    write_temp.append(doc_answer_sim[query][doc])
                else:
                    write_temp.append(0.)
                write_temp.append(MixedSim[query][doc])
                writer.writerow(write_temp)
                if answer_num == 20:
                    break
            # if answer_num < 20:
            #     print(query)


title_answer = {}  # 保存只用title信息得到的文档
title_answer_sim = {}  # 文档对应的相似度
doc_answer = {}
doc_answer_sim = {}
query_id = []
loadAnswer()
MixedSim = {}
getMixedSim()
outputSubmission()
