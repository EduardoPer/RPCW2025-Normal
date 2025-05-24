# RPCW2025-Normal
# Criacao no protege
no protege, criei as relacoes e classes recomendadas pelo professor, para além das inversas a essas (menos da :estáRelacionadoCom) e as data properties :titulo, :nome e :idade
(Nota: No povoamento dos aprendizes, por lapso, coloquei os seus nomes na data property ":titulo")

# Povoamento:
Para cada dataset, adicionei novas instancias das classes de cada objeto, quer seja a key, quer seja objetos relacionados (por exemplo, no "obras", adicionei instancias da classe "Obra", e ainda adicionei Mestres e Conceitos. Sempre a verificar se estes campos existem, e se sim, se já estão criados.)

Para correr o script, usar python3 povoarOnt.py

# Queries:
(localizadas no ficheiro sparql.txt, e as INSERT/CONSTRUCT no migrations.py)
- Para a query 12, escolhi o mestre "Pierre Bourdieu".

- Para a query 22, utilizei a função "GROUP_CONCAT", que permite agrupar todas as instancias numa só, separadas por um separador.

- Para a query 23, utilizei BIND(IF...) de forma a testar as idades e fazer a correspondencia com uma faixa.