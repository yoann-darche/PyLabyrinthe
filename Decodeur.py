# -*- coding: utf-8 -*-

def DecodeMsg(Buffer):
    """
    Cette fonction assure le décodage d'un buffer. Elle decode le premier message
    complet et retourne le reste du buffer. Si le buffer est incomplet pour le
    décodage alors le buffer retourné sera inchangé. Si le buffer ne commence pas
    par une entête de message alors le debut du buffer jusqu'à la fin d'un message
    ou le début du suivant sera nettoyé.
    """

    Instruction = None
    
    # Vérification que le buffer n'est pas null
    if Buffer is None or Buffer == '':
        return ('', None)

    # Recherche du premier caractère '{'
    lpos = Buffer.find('{');
    if lpos < 0:
        return ('', None)
    else:
        Buffer = Buffer[lpos+1:];
        # Recherche de la fin de l'instruction
        rpos = Buffer.find('}');
        if rpos < 0:
            return ('{'+Buffer, None)
        else:
            # Décodage de l'instruction
            ITemp = Buffer[:rpos].split(':')
            Buffer = Buffer[rpos+1:]
            # Nettoyage de la liste des instructions
            for i,a in enumerate(ITemp):
                ITemp[i] = a.strip()
                
            while ITemp.count('') > 0:
                ITemp.remove('')

            if len(ITemp) == 0:
                ITemp = None

    

        
    return (Buffer, ITemp)



# ########################################################
# ## TEST Unitaires                                     ##
# ########################################################

if __name__ == "__main__":


    Msg = "BlaBla"
    print(Msg," : ", DecodeMsg(Msg));
    
    Msg = "STOP}"
    print(Msg," : ", DecodeMsg(Msg));

    Msg = "{STOP"
    print(Msg," : ", DecodeMsg(Msg));
    
    Msg = "{STOP}"
    print(Msg," : ", DecodeMsg(Msg));

    Msg = "{STOP}{START}"
    print(Msg," : ", DecodeMsg(Msg));

    Msg = "{ELO:192.168.10.1}"
    print(Msg," : ", DecodeMsg(Msg));

    Msg = "LeBlaBla{ELO:192.168.10.1}Et la j'en remet un peu"
    print(Msg," : ", DecodeMsg(Msg));

    Msg = "LeBlaBla{ELO:192.168.10.1}Et la j'en remet un peu"+ \
          "LeBlaBla{TOTO:Param1: Param2:P3:}Et la j'en remet un peu"+ \
          "zz zzz zzz {} xxxx {TITI: P01:P02 : P03 : :: } oooo"
          
    while Msg != '':
        print(Msg,end='')
        Msg, Inst = DecodeMsg(Msg)
        print(" : ", Inst);

        
