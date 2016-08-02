# -*- coding: utf-8 -*-
# TESTS LIT TO SEARCH
def analisi_filtrate():
    # HIDE DB FIELDS
    db.esami.id.readable = False
    # QUERY THE DB
    query = (
    db.esami.analita.contains(request.vars.Cerca_prestazione) | db.esami.search_keywords.contains(request.vars.Cerca_prestazione))

    campi = [db.esami.id, db.esami.analita, db.materiali.materiale, db.esami.obsoleto]
    intestazione = {'esami.id': 'ID',
                    'esami.analita': 'Descrizione',
                    'esami.obsoleto': 'Non più eseguito',
                    }
    # SORT ORDER
    ordinamento = [db.esami.analita]
    # lunghezza campi
    lunghezza = {'esami.analita': 60, 'esami.obsoleto': 5}
    # LINK OTHER TABLE
    left = db.esami.on(db.esami.id_materiali == db.materiali.id)
    # DISPLAY ADDITIONAL LINKS
    links = [
        lambda row: A('Visualiza', _href=URL('default', 'scheda_esami', args=[row('esami.id')]), _class='btn btn-info')]

    # BULD THE GRID
    grid = SQLFORM.grid(query=query, left=left, fields=campi,
                        headers=intestazione, orderby=ordinamento,
                        links=links,
                        create=False, deletable=False,
                        editable=False, details=False, paginate=20,
                        maxtextlength=lunghezza, csv=False)
    return dict(lista=grid)


@auth.requires_membership('superuser')
def unop():  # department managment
    grid = SQLFORM.grid(db.unitaoperativa, deletable=False, maxtextlength={'unitaoperativa.descrizione': 60})
    return locals()


@auth.requires_membership('superuser')
def gen_cfg():  # general pharameters configuration
    grid = SQLFORM.grid(db.cfg_gen, deletable=False, details=False)
    return locals()


@auth.requires_login()
def mat():  # materials managements
    db.materiali._common_filter = lambda query: db.materiali.id_unitaoperativa == auth.user.id_unitaoperativa
    grid = SQLFORM.grid(db.materiali, deletable=False, details=False, maxtextlength={'materiali.materiale': 60},
                        paginate=50)
    return locals()


@auth.requires_login()
def sett():  # sub-departemens managements
    db.settori._common_filter = lambda query: db.settori.id_unitaoperativa == auth.user.id_unitaoperativa
    grid = SQLFORM.grid(db.settori, deletable=False, details=False, maxtextlength={'settori.settore': 60}, paginate=50)
    return locals()


@auth.requires_login()
def cont():  # tubes management
    db.contenitori._common_filter = lambda query: db.contenitori.id_unitaoperativa == auth.user.id_unitaoperativa
    grid = SQLFORM.grid(db.contenitori, deletable=False, details=False, maxtextlength={'contenitori.contenitore': 60},
                        paginate=50)
    return locals()


@auth.requires_login()
def metod():  # griglia di editing ed inserimento motodi
    db.metodi._common_filter = lambda query: db.metodi.id_unitaoperativa == auth.user.id_unitaoperativa
    grid = SQLFORM.grid(db.metodi, deletable=False, details=False, maxtextlength={'metodi.metodo': 60}, paginate=50)
    return locals()


@auth.requires_membership('superuser')
def ges_user():
    db.auth_user.id_unitaoperativa.writable = True
    db.auth_user.id_unitaoperativa.readable = True
    grid = SQLFORM.grid(db.auth_user, deletable=False, details=False)
    return locals()


# Tests managemnt

@auth.requires_login()  # todo
def lis_anal():  # anlites list to edit
    db.esami._common_filter = lambda query0: db.esami.id_unitaoperativa == auth.user.id_unitaoperativa
    db.materiali._common_filter = lambda query1: db.materiali.id_unitaoperativa == auth.user.id_unitaoperativa
    db.settori._common_filter = lambda query2: db.settori.id_unitaoperativa == auth.user.id_unitaoperativa
    db.contenitori._common_filter = lambda query3: db.contenitori.id_unitaoperativa == auth.user.id_unitaoperativa
    db.metodi._common_filter = lambda query4: db.metodi.id_unitaoperativa == auth.user.id_unitaoperativa
    left = db.esami.on((db.esami.id_materiali == db.materiali.id) & (db.esami.id_settore == db.settori.id))

    # REORDER OF FROM'S FILESDS
    edit_args =[
        #main fields
        'analita',
        'search_keywords',
        'attivo',
        'id_unitaoperativa',
        'id_materiali',
        'id_contenitore',
        'id_metodo',
         'id_settore',
        'codice_metafora',
        'codice_DM',
        'tariffa_DM',
        #-------------------
        'eseguibile_urgenza',
        'eseguibile_routine',
        'eseguibile_esterni',
        'prenotazione',
        'service',
        'obsoleto',
        #----------------------
        'preparazione_paziente',
        'moduli_richiesta',
        'raccolta',
        'volume_minimo',
        'unita_misura',
        'trasporto',
        #----------------------
        'unita_misura',
        'riferimento',
        'interpretazione',
        'interferenze',
        'giorni_effettuazione',
        'udm_tempo_attesa',
        'tempo_refertazione',
        'tempo_refertazione_urgenza',
        'conservazione',
        #--------------------
        'veq',
        'note',
        'numero_revisione',
        ] # order of fields in edit form


    grid = SQLFORM.grid(
        db.esami,
        left=left, deletable=False, details=False, paginate=50, showbuttontext=False,
        fields=[db.materiali.sigla, db.esami.analita, db.settori.settore, db.esami.attivo],
        editargs={'fields': edit_args},
        createargs={'fields': edit_args},
        maxtextlength={'materiali.sigla': 4}
    )
    return locals()

# _____________________________
