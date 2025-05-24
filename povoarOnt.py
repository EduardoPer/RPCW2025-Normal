import csv, re, json
from rdflib import RDF, RDFS, OWL, Graph, Namespace, URIRef, Literal, XSD

n = Namespace("http://rpcw.di.uminho.pt/2025/sapientia#")
g = Graph()
g.parse("sapientia_base.ttl")

with open("conceitos.json", "r", encoding="utf-8") as f:
    conceitos_dict = json.load(f)

conceitos = []
disciplinas = []
mestres = []
obras = []
aprendizes = []
aplicacoes = []
periodos = []
tipos_conhecimento = []
for conceito in conceitos_dict["conceitos"]:
    conceito_aux = "Conceito_" + (conceito["nome"].strip().replace(" ", "_"))
    conceitoURI = URIRef(f"{n}{conceito_aux}")
    
    if conceitoURI not in conceitos:
        conceitos.append(conceitoURI)
        g.add((conceitoURI, RDF.type, OWL.NamedIndividual))
        g.add((conceitoURI, RDF.type, n.Conceito))
        g.add((conceitoURI, n.nome, Literal(conceito["nome"], datatype=XSD.string)))
    
    if conceito.get("aplicações"):
        for aplicacao in conceito["aplicações"]:
            aplicacao_aux = "Aplicação_" + (aplicacao.strip().replace(" ", "_"))
            aplicacaoURI = URIRef(f"{n}{aplicacao_aux}")
            if aplicacaoURI not in aplicacoes:
                aplicacoes.append(aplicacaoURI)
                g.add((aplicacaoURI, RDF.type, OWL.NamedIndividual))
                g.add((aplicacaoURI, RDF.type, n.Aplicação))
                g.add((aplicacaoURI, n.nome, Literal(aplicacao, datatype=XSD.string)))
            g.add((conceitoURI, n.temAplicaçãoEm, aplicacaoURI))
            g.add((aplicacaoURI, n.éAplicaçãoDe, conceitoURI))
    
    if conceito.get("períodoHistórico"):
        per_aux = "PeríodoHistorico_" + (conceito["períodoHistórico"].strip().replace(" ", "_"))
        perURI = URIRef(f"{n}{per_aux}")
        if perURI not in periodos:
            periodos.append(perURI)
            g.add((perURI, RDF.type, OWL.NamedIndividual))
            g.add((perURI, RDF.type, n.PeríodoHistorico))
            g.add((perURI, n.nome, Literal(conceito["períodoHistórico"], datatype=XSD.string)))
        g.add((conceitoURI, n.surgeEm, perURI))
        g.add((perURI, n.éPeríodoDe, conceitoURI))
    
    for rel_con in conceito["conceitosRelacionados"]:
        rel_aux = "Conceito_" + (rel_con.strip().replace(" ", "_"))
        relURI = URIRef(f"{n}{rel_aux}")
        if relURI not in conceitos:
            conceitos.append(relURI)
            g.add((relURI, RDF.type, OWL.NamedIndividual))
            g.add((relURI, RDF.type, n.Conceito))
            g.add((relURI, n.nome, Literal(rel_con, datatype=XSD.string)))
        g.add((conceitoURI, n.estáRelacionadoCom, relURI))

conceitos_dict = {}
with open("disciplinas.json", "r", encoding="utf-8") as f:
    disciplinas_dict = json.load(f)

for disc in disciplinas_dict["disciplinas"]:
    disc_aux = "Disciplina_" + (disc["nome"].strip().replace(" ", "_"))
    discURI = URIRef(f"{n}{disc_aux}")
    if discURI not in disciplinas:
        disciplinas.append(discURI)
        g.add((discURI, RDF.type, OWL.NamedIndividual))
        g.add((discURI, RDF.type, n.Disciplina))
        g.add((discURI, n.nome, Literal(disc["nome"], datatype=XSD.string)))
    
    if disc.get("tiposDeConhecimento"):
        for tc in disc["tiposDeConhecimento"]:
            tc_aux = "TipoDeConhecimento_" + (tc.strip().replace(" ", "_"))
            tcURI = URIRef(f"{n}{tc_aux}")
            if tcURI not in tipos_conhecimento:
                tipos_conhecimento.append(tcURI)
                g.add((tcURI, RDF.type, OWL.NamedIndividual))
                g.add((tcURI, RDF.type, n.TipoDeConhecimento))
                g.add((tcURI, n.nome, Literal(tc, datatype=XSD.string)))
            g.add((discURI, n.pertenceA, tcURI))
            g.add((tcURI, n.temDisciplina, discURI))
            
    if disc.get("conceitos"):
        for con in disc["conceitos"]:
            con_aux = "Conceito_" + (con.strip().replace(" ", "_"))
            conURI = URIRef(f"{n}{con_aux}")
            if conURI not in conceitos:
                conceitos.append(conURI)
                g.add((conURI, RDF.type, OWL.NamedIndividual))
                g.add((conURI, RDF.type, n.Conceito))
                g.add((conURI, n.nome, Literal(con, datatype=XSD.string)))
            g.add((conURI, n.éEstudadoEm, discURI))
            g.add((discURI, n.estudaConceito, conURI))

disciplinas_dict = {}
with open("mestres.json", "r", encoding="utf-8") as f:
    mestres_dict = json.load(f)

for mestre in mestres_dict["mestres"]:
    mestre_aux = "Mestre_" + (mestre["nome"].strip().replace(" ", "_"))
    mestreURI = URIRef(f"{n}{mestre_aux}")
    if mestreURI not in mestres:
        mestres.append(mestreURI)
        g.add((mestreURI, RDF.type, OWL.NamedIndividual))
        g.add((mestreURI, RDF.type, n.Mestre))
        g.add((mestreURI, n.nome, Literal(mestre["nome"], datatype=XSD.string)))
    
    if mestre.get("períodoHistórico"):
        per_aux = "PeríodoHistorico_" + (mestre["períodoHistórico"].strip().replace(" ", "_"))
        perURI = URIRef(f"{n}{per_aux}")
        if perURI not in periodos:
            periodos.append(perURI)
            g.add((perURI, RDF.type, OWL.NamedIndividual))
            g.add((perURI, RDF.type, n.PeríodoHistorico))
            g.add((perURI, n.nome, Literal(conceito["períodoHistórico"], datatype=XSD.string)))
        g.add((mestreURI, n.foiMestreEm, perURI))
        g.add((perURI, n.foiPeríodoDoMestre, mestreURI))
    
    if mestre.get("disciplinas"):
        for disc in mestre["disciplinas"]:
            disc_aux = "Disciplina_" + (disc.strip().replace(" ", "_"))
            discURI = URIRef(f"{n}{disc_aux}")
            if discURI not in disciplinas:
                disciplinas.append(discURI)
                g.add((discURI, RDF.type, OWL.NamedIndividual))
                g.add((discURI, RDF.type, n.Disciplina))
                g.add((discURI, n.nome, Literal(disc, datatype=XSD.string)))
            g.add((mestreURI, n.ensina, discURI))
            g.add((discURI, n.éEnsinadaPor, mestreURI))

mestres_dict = {}
with open("obras.json", "r", encoding="utf-8") as f:
    obras_dict = json.load(f)
    
for obra in obras_dict["obras"]:
    obra_aux = "Obra_" + (obra["titulo"].strip().replace(" ", "_"))
    obraURI = URIRef(f"{n}{obra_aux}")
    if obraURI not in obras:
        obras.append(obraURI)
        g.add((obraURI, RDF.type, OWL.NamedIndividual))
        g.add((obraURI, RDF.type, n.Obra))
        g.add((obraURI, n.titulo, Literal(obra["titulo"], datatype=XSD.string)))
    
    if obra.get("autor"):
        autor_aux = "Mestre_" + (obra["autor"].strip().replace(" ", "_"))
        autorURI = URIRef(f"{n}{autor_aux}")
        if autorURI not in mestres:
            mestres.append(autorURI)
            g.add((autorURI, RDF.type, OWL.NamedIndividual))
            g.add((autorURI, RDF.type, n.Mestre))
            g.add((autorURI, n.nome, Literal(obra["autor"], datatype=XSD.string)))
        g.add((obraURI, n.foiEscritoPor, autorURI))
        g.add((autorURI, n.escreveuObra, obraURI))
    
    if obra.get("conceitos"):
        for con in obra["conceitos"]:
            con_aux = "Conceito_" + (con.strip().replace(" ", "_"))
            conURI = URIRef(f"{n}{con_aux}")
            if conURI not in conceitos:
                conceitos.append(conURI)
                g.add((conURI, RDF.type, OWL.NamedIndividual))
                g.add((conURI, RDF.type, n.Conceito))
                g.add((conURI, n.nome, Literal(con, datatype=XSD.string)))
            g.add((obraURI, n.explica, conURI))
            g.add((conURI, n.éExplicadoPor, obraURI))

obras_dict = {}
with open("pg53797.json", "r", encoding="utf-8") as f:
    aprendizes_list = json.load(f)

for aprendiz in aprendizes_list:
    ap_aux = "Aprendiz_" + (aprendiz["nome"].strip().replace(" ", "_"))
    apURI = URIRef(f"{n}{ap_aux}")
    
    if apURI not in aprendizes:
        aprendizes.append(apURI)
        g.add((apURI, RDF.type, OWL.NamedIndividual))
        g.add((apURI, RDF.type, n.Aprendiz))
        g.add((apURI, n.titulo, Literal(aprendiz["nome"], datatype=XSD.string)))
        g.add((apURI, n.idade, Literal(aprendiz["idade"], datatype=XSD.integer)))
    
    if aprendiz.get("disciplinas"):
        for disc in aprendiz["disciplinas"]:
            disc_aux = "Disciplina_" + (disc.strip().replace(" ", "_"))
            discURI = URIRef(f"{n}{disc_aux}")
            if discURI not in disciplinas:
                disciplinas.append(discURI)
                g.add((discURI, RDF.type, OWL.NamedIndividual))
                g.add((discURI, RDF.type, n.Disciplina))
                g.add((discURI, n.nome, Literal(disc, datatype=XSD.string)))
            g.add((apURI, n.aprende, discURI))
            g.add((discURI, n.éAprendidaPor, apURI))
    
        
g.serialize(destination="sapientia_ind.ttl", format="turtle", encoding="utf-8")