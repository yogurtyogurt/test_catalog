##variabili e stringhe di sistema
db.define_table('cfg_gen',
                Field('funct','string',length=255,required=True,
                      requires=IS_NOT_IN_DB(db,'cfg_gen.funct')),
                Field('valore','text',required=True),
                Field('description','text',required=True),
                auth.signature,
                format='%(funct)s',

               )

#general pharameters
SITE_TITLE=T("Tests catalog")
