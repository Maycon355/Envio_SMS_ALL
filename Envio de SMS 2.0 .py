import time
import vonage
import cx_Oracle

#PARAMETROS PARA A USABILIDADE DA API 
client = vonage.Client(key="*", secret="*")
sms = vonage.Sms(client)
time.sleep(10)

#FUNÇÃO PARA ENVIO DA MENSAGEM *LÓGICA*
def send():
    Texto = ('[AVISO GTFOODS]' + '\n' + Cliente.strip() + ' sua carga foi faturada, vai ser entregue em 24hrs' )
    responseData = sms.send_message(
        {
            "from": "GTFOODS",
            "to": Telefone,
            "text": Texto,
            }
    )
    arquivo = open('C:\\Users\\maycon.silva1\\Desktop\\Envio de SMS Projeto\\Logarq01.txt','a')

    if responseData["messages"][0]["status"] == "0":
        print("Mensagem enviada com sucesso " + Telefone +' - ' + Cliente.strip())
        time.sleep(15)
    else:
        print(f"Falha na mensagem com erro: {responseData['messages'][0]['error-text']} " + " - "+ Telefone)
        arquivo.write('Número incorreto |'+ Telefone +'|'+' COM ERRO' + "\n")
        print ("\nLog Salvo:  " + arquivo.name + " | ") 
        time.sleep(15)

# -------------------------------------------------
#   REALIZANDO CONEXÃO COM O BANCO DE DADOS PROTHEUS / INTEGRAÇÃO / CX_ORACLE
# -------------------------------------------------

dsn_tns = cx_Oracle.makedsn('host', 'port', service_name='id') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
con = cx_Oracle.connect(user=r'*', password='*', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
consulta = con.cursor()
consulta.execute("""SELECT DISTINCT
    TRIM(REGEXP_REPLACE(concat('+55'|| SA1.A1_DDD,SA1.A1_TEL),'\s*', '')) AS "DDD + TELEFONE", -- campos[0]
    SA1.A1_END AS ENDERECO, ------------------------------------------------------------------- campos[1]
    SA1.A1_NREDUZ AS NOME, -------------------------------------------------------------------- campos[2]
    TRIM(B1_DESC) AS DESCRICAO_02, ------------------------------------------------------------ campo [3]
    PAD.PAD_DATA
FROM
  TMPROD.PAD010 PAD
LEFT JOIN
      TMPROD.pa1010 pa1 ON
      PAD.PAD_LOTEAV = pa1.pa1_xltav
LEFT JOIN TMPROD.SA1010 SA1 ON
     SA1.A1_COD = PA1.PA1_FORNEC
INNER JOIN
      TMPROD.SB1010 SB1 ON
      SB1.B1_FILIAL = SB1.B1_FILIAL AND
      B1_COD = PAD.PAD_PRODU AND
      SB1.D_E_L_E_T_ = ' '
     
WHERE PAD.D_E_L_E_T_ = ' ' 
    AND TO_DATE (PAD.PAD_DATA, 'YYYYMMDD') = TO_DATE(SYSDATE)
    AND TRIM(PA1.PA1_DTFECH) IS NULL 
    AND PAD.PAD_PRODU IN ('SUBRACMI000031','SUBRACMI000004','SUBRACMI000001','SUBRACMI000002','SUBRACMI000028','SUBRACMI000005','SUBRACMI000003','SUBRACMI000017','MCINS000116','SUBRACMI000007','SUBRACMI000032','SUBRACMI000006','SUBRACMI000008','SUBRACMI000016','MCINS000019')
    AND TRIM(PA1.PA1_DTFECH) IS NULL""")

retorno = consulta.fetchall()

for campos in (retorno):      
   Telefone = campos[0] # Primeiro campo da consulta SQL
   Endereco = campos[1] # Segundo campo da consulta SQL
   Cliente =  campos[2] # Terceiro campo da consulta SQL
   time.sleep(15)
        
   if send(): # Valida se o site do Whastapp está online
        print('Mensagem enviada com sucesso para o número: ' + Telefone)# Envia a mensagem
        time.sleep(5)



   