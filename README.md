Python script for conjugating regular verbs in Irish. Just pass in the verb as an argument for the script. Has no understand of irregular verbs, so if you put in "feic" expect to get "d'fheic mé" as the past tense.


## usage:

    reimnigh.py [OPTIONS] [VERB]

By default will show all persons in all tenses in affirmative, negative and interrogative forms. Use options to narrow the output. There is also an option for the Munster dialect.

    -c aimsir chaite / past tense
    -g aimsir ghnáthchaite / imperfect tense
    -l aimsir láithreach / present tense
    -f aimsir fháistineach / future tense
    -F modh foshuiteach / subjunctive mood
    -o modh ordaitheach / imperative mood
    -O modh coinníollach / conditional mood

    -1 céad phearsa / first person
    -2 dara pearsa / second person
    -3 tríú pearsa / third person
    -0 briathar saor / automonous form
    -u uatha / singular
    -i iolra / plural

    -d foirm dhearfach / affirmative form
    -D foirm dhiúltach / negative form
    -C foirm cheisteach / interrogative form

    -m chanúint na Mumhan / Munster dialect

## examples:

    $ python reimnigh.py eitil -1ucd
    > d'eitil mé
    $ python reimnigh.py eitil -1ucdm
    > d'eitlíos
    $ python reimnigh.py beannaigh -30fC
    > an mbeannóidh sí      
    > an mbeannóidh sé      
    > an mbeannóidh siad    
    > an mbeannófar
    $python reimnigh.py léim -2iclf
    >  an aimsir chaite
    >léim sibh        níor léim sibh      ar léim sibh        
    >
    >  an aimsir láithreach
    >léimeann sibh    ní léimeann sibh    an léimeann sibh    
    >
    >  an aimsir fháistineach
    >léimfidh sibh    ní léimfidh sibh    an léimfidh sibh


- Writen by Caoimhe Ní Chaoimh, © 2020
- License: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International][CC BY-NC-SA 4.0]

[CC BY-NC-SA 4.0]: https://creativecommons.org/licenses/by-nc-sa/4.0/
