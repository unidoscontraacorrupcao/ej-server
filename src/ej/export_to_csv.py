import csv
from django.core.files.base import ContentFile

from ej_users.models import User
from ej_profiles.models import Profile
from ej_missions.models import Mission, Receipt
from ej_candidates.models.candidate import Candidate
from ej_candidates.models.selected_candidates import SelectedCandidate
from ej_candidates.models.pressed_candidates import PressedCandidate

USERS_CSV_FILE_PATH = '/tmp/usuarios_exportados.csv'
CANDIDATES_CSV_FILE_PATH = '/tmp/candidatos_exportados.csv'


def export_users():
    with open(USERS_CSV_FILE_PATH, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['nome',
            'email',
            'cidade',
            'estado',
            'genero',
            'raça',
            'telefone',
            'idade',
            'candidatos_selecionados',
            'candidatos_pressionados',
            'missoes_realizadas',
            'missoes_aceitas'
            ])
        profiles = Profile.objects.select_related('user')
        for profile in profiles:
            selected_candidates = list(map(lambda candidate: candidate.candidate_id,
                SelectedCandidate.objects.filter(user_id=profile.user_id)))
            pressed_candidates = list(map(lambda candidate: candidate.candidate_id,
                PressedCandidate.objects.filter(user_id=profile.user_id)))
            realized_missions = list(map(lambda receipt: receipt.mission.title,
                Receipt.objects.filter(status="realized", user=profile.user_id)))
            accepted_missions = list(map(lambda mission: mission.title,
                Mission.objects.filter(users__id=profile.user_id)))
            spamwriter.writerow([profile.user.display_name,
                profile.user.email,
                profile.city,
                profile.state,
                translate_gender(profile.gender.value),
                translate_race(profile.race.value),
                profile.phone,
                profile.age,
                selected_candidates,
                pressed_candidates,
                realized_missions,
                accepted_missions])
            print("Usuário " + profile.user.display_name +  "exportado")

def translate_gender(gender):
    options = {
        0:"Não declarado",
        1:"Feminino",
        2:"Masculino",
        3:"Feminino CIS",
        4:"Masculino CIS",
        5:"Agenero",
        6:"Queer",
        7:"Gênero Fluido",
        8:"Gênero não conformista",
        9:"Genero variante",
        10:"Intersexo",
        11:"Não binário",
        12:"Transgênero",
        13:"Pangênero",
        14:"Transexual Mulher",
        15:"Transexual Homem",
        16:"Transfeminino",
        17:"Transmasculino",
        18:"Não sabe",
        19:"Nenhum",
        20:"Outros"
    }
    return options[gender]

def translate_race(race):
    options = {
        0:'Não declarado',
        1:'Negro',
        2:'Pardo',
        3:'Branco',
        4:'Amarelo',
        5:'Indígena',
        6:'Não sabe'
    }

    return options[race]

def export_candidates():
    with open(CANDIDATES_CSV_FILE_PATH, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id',
            'cpf',
            'nome_urna',
            'uf',
            'passado_limpo',
            'pacto_democracia',
            'novas_medidas',
            'n_selecionados',
            'n_pressionados',
            ])
        candidates = Candidate.objects.all()
        for candidate in candidates:
            n_selecionados = len(list(map(lambda candidate: candidate.candidate_id,
                SelectedCandidate.objects.filter(candidate_id=candidate.id))))
            n_pressionados = len(list(map(lambda candidate: candidate.candidate_id,
                PressedCandidate.objects.filter(candidate_id=candidate.id))))
            spamwriter.writerow([
                candidate.id,
                candidate.cpf,
                candidate.name,
                candidate.uf,
                candidate.has_clean_pass,
                candidate.committed_to_democracy,
                candidate.adhered_to_the_measures,
                n_selecionados,
                n_pressionados])
            print("Candidato " + candidate.name +  " exportado")

def export():
    export_users()
    export_candidates()
    print("dados dos usuários exportados em: ", USERS_CSV_FILE_PATH)
    print("dados dos candidatos exportados em: ", CANDIDATES_CSV_FILE_PATH)

if __name__ == '__main__':
    export()
