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
        0:"UNDECLARED",
        1:"FEMALE",
        2:"MALE",
        3:"CIS_FEMALE",
        4:"CIS_MALE",
        5:"AGENDER",
        6:"GENDERQUEER",
        7:"GENDERFLUID",
        8:"NON_CONFORMIST_GENDER",
        9:"VARIANT_GENDER",
        10:"INTERSEX",
        11:"NON_BINARY",
        12:"TRANSGENDERED",
        13:"PANGENDER",
        14:"TRANSSEXUAL_WOMAN",
        15:"TRANSSEXUAL_MAN",
        16:"TRANSFEMINAL",
        17:"TRANSMASCULINE",
        18:"DO_NOT_KNOW",
        19:"NONE",
        20:"OTHER"
    }
    return options[gender]

def translate_race(race):
    options = {
        0:'Undeclared',
        1:'Black',
        2:'Brown',
        3:'White',
        4:'Yellow',
        5:'Indigenous',
        6:'Do not know'
    }

    return options[race]

def export_candidates():
    with open(CANDIDATES_CSV_FILE_PATH, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['id',
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
