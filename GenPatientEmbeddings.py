import csv, time

from Entities import Hpo, HpoVecs
from Common import save_object

def compute_embedding_average(phenotype, hpo, hpo_vectors):
    lenght = len(phenotype)
    suma = 0
    for symptom in phenotype:
        hpo_id = hpo.id(symptom)
        vector_id = hpo_vectors[hpo_id]
        suma += vector_id
    return suma/lenght

<<<<<<< HEAD
def gen_patient_embeddings(source, enriched, EXP_ID, exp_id):
=======
def gen_patient_embeddings(source, exp_id):
>>>>>>> 188da1ede0252aaddfb2c655d07e5a6fd96a961c
    start = time.time()

    with open('./_data/patients/'+source+'_patients_phenotype.csv') as csv_file:
        patient_sims = csv.reader(csv_file)
        hpo = Hpo()
<<<<<<< HEAD
        hpo_vectors = HpoVecs(enriched, EXP_ID, exp_id).vecs
=======
        hpo_vectors = HpoVecs(exp_id).vecs
>>>>>>> 188da1ede0252aaddfb2c655d07e5a6fd96a961c
        patients = {}
        for line in patient_sims:
            patients[line[0]] = compute_embedding_average(line[1:], hpo, hpo_vectors)

    save_object(patients, './_data/patients/'+source+'_patient_embeddings.pkl')

    print(time.time()-start)
