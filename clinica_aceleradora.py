from datetime import datetime
import sys


#entities
class Patient:
  def __init__(self, name, phone):
    self.name = name
    self.phone = phone

  def set_appointment_medical(self, appointment):
    self.appointment = appointment


class Appointment:
  def __init__(self, speciality, date, hour):
    self.speciality = speciality
    self.date = date
    self.hour = hour


#list/variables
list_patient = []
list_patient_appointment = []
message = "Insira uma das opções"
invalid_option = "Opção inválida, tente novamente"

datas_appointment = {
  'medical_speciality': [
      'ortopedia',
      'dermatologia',
      'cardiologia',
      'pneumologia'
   ],
  'date': [
      datetime(2023, 10, 1),
      datetime(2023, 10, 2),
      datetime(2023, 10, 3),
      datetime(2023, 10, 4)
  ],
  'hour': ['8:00', '9:00', '10:00', '11:00']
}

#services
def show_iteration(list_args, attr=""):
  for id, item in enumerate(list_args):
    value = getattr(item, attr, None)
    print(id + 1, " - ", value) if value is not None else print(id + 1, " - ", item)


def validate_date():
  for id, date in enumerate(datas_appointment['date']):
    print(date.strftime("%d/%m/%Y"))

  current_date = datetime.now().date()
  choice_date = input("\nInsira a data da consulta (dd/mm/aaaa): ")
  choice_date = datetime.strptime(choice_date, "%d/%m/%Y").date()
  formatted_dates = [date.strftime("%Y-%m-%d") for date in datas_appointment['date']]

  while current_date > choice_date:
    print("\nVocê não pode agendar datas retroativas")
    choice_date = input("Insira a data da consulta (dd/mm/aaaa): ")
    choice_date = datetime.strptime(choice_date, "%d/%m/%Y").date()

  while choice_date.strftime("%Y-%m-%d") not in formatted_dates:
    print("\nData indisponível")
    choice_date = input("Insira a data da consulta (dd/mm/aaaa): ")
    choice_date = datetime.strptime(choice_date, "%d/%m/%Y").date()
    
  return choice_date


#application
def register_patient():
  noCadastre = True
  name = input("\nDigite seu nome: ")
  phone = input("Digite seu número de telefone com 9 dígitos: ")

  while not len(phone) == 9:
    print("\nNumero de telefone inválido")
    phone = input("Digite seu número de telefone com 9 dígitos: ")

  for patient in list_patient:
    if patient.phone == phone:
      print("\nPaciente já cadastrado!\n")
      noCadastre = False
      break

  if len(list_patient) == 0 or noCadastre == True:
    new_patient = Patient(name, phone)
    print("\nPaciente cadastrado com sucesso\n")
    list_patient.append(new_patient)
  menu()


def make_appointment():
  print("\nLista de Pacientes:")
  show_iteration(list_patient, "name")
  option_patient = int(input(message + " referente ao paciente: "))

  while option_patient < 1 or option_patient > len(list_patient):
      print("\n" + invalid_option)
      option_patient = int(input(message + " referente ao paciente: "))

  chosen_patient = list_patient[option_patient - 1]

  print("\nLista de Especialidades:")
  show_iteration(datas_appointment['medical_speciality'])
  choice_speciality = int(input(message + " referente a especialidade: "))

  while choice_speciality not in range(1, len(datas_appointment['medical_speciality']) + 1):
    print("\n" + invalid_option)
    choice_speciality = int(input(message + " referente a especialidade: "))

  repeat = True
  while repeat:
    repeat = False
    print("\nOpções de datas para consulta: ")
    choice_date = validate_date()

    print("\nOpções de horários para consulta: ")
    show_iteration(datas_appointment['hour'])
    choice_hour = int(input(message + " referente a hora: "))
  
    while choice_hour not in range(1, len(datas_appointment['hour']) + 1):
      print("\n" + invalid_option)
      choice_hour = int(input(message + " referente a hora: "))
  
    for booked in list_patient_appointment:
      if (choice_date == booked.appointment.date) and (datas_appointment['hour'][choice_hour - 1] == booked.appointment.hour):
          print("\nData e hora não disponível, favor tente novamente")
          repeat = True


  new_appointment = Appointment(
      datas_appointment['medical_speciality'][choice_speciality - 1],
      choice_date,
      datas_appointment['hour'][choice_hour - 1]
  )

  for item in list_patient:
    if chosen_patient.name == item.name:
      item.set_appointment_medical(new_appointment)
      list_patient_appointment.append(item)
      print("\nAgendamento realizado com sucesso\n")
      menu()
      break


def cancel_appointment():
  print("\nLista de Agendamentos:")
  show_iteration(list_patient_appointment, "name")
  selected = int(input("Informe o paciente que deseja remarcar a consulta: "))

  for id, data in enumerate(list_patient_appointment):
    if(selected == id + 1):
      print("\nDados da consulta do paciente selecionado:")
      print("nome:", data.name, "\n"
            "data:", data.appointment.date.strftime("%d/%m/%Y"), "\n"
            "hora:", data.appointment.hour, "\n"
            "especialidade médica:", data.appointment.speciality)

      resposta = input("Deseja cancelar a consulta? (s/n) ")
      while(resposta != "s" or "n"):
        if resposta == "s":
          list_patient_appointment.pop(id)
          print("\nConsulta cancelada com sucesso.\n")
          menu()
          break
        elif resposta == "n":
          print("\nA consulta não foi cancelada.\n")
          menu()
          break
        else:
          print("\n" + invalid_option)
          resposta = input("Deseja cancelar a consulta? (s/n) ")


def exit():
  sys.exit()


def execute_choice(choice):
  if choice == 1:
    register_patient()
  elif choice == 2:
    make_appointment()
  elif choice == 3:
    cancel_appointment()
  elif choice == 4:
    exit()


def menu():
  print("------------------------------")
  print("CLÍNICA ACELERADORA")
  print("------------------------------\nEscolha uma das opções abaixo.")
  print("1. CADASTRAR PACIENTE")
  print("2. AGENDAR CONSULTA")
  print("3. CANCELAR CONSULTA")
  print("4. SAIR")
  print("------------------------------")
  choice_user = int(input("Digite uma opção do menu: "))

  if (choice_user < 1 or choice_user > 4):
    print("-----------------------------")
    print("escolha uma opção entre 1 a 4")
    print("-----------------------------")
    menu()
  else:
    execute_choice(choice_user)


menu()