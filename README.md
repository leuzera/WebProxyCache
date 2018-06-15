# WebProxyCache

Nesse trabalho, o objetivo é criar um proxy Web cache que ofereça seus serviços em duas portas TCP (Transmission Control Protocol) diferentes: uma para comunicação HTTP (54321) e outra para monitoramento básico (54322).
Na porta TCP 54321, o proxy Web deverá aceitar conexões a partir das quais serão enviadas requisições HTTP e suas respostas correspondentes.
Na porta TCP 54322, o proxy Web deverá apresentar informações básicas de seu uso.
Por exemplo: há quanto tempo o servidor está no ar; um ranking dos sites mais visitados; ranking dos maiores objetos armazenados; ranking dos objetos mais requisitados, etc.
A lista completa de informações apresentadas, a quantidade de itens apresentados, o projeto da interface exibida, etc. devem fazer parte da documentação do trabalho e deverão ser definidos por cada grupo.

O proxy Web deverá estar de acordo com a especificação do HTTP/1.1 conforme descrito no documento RFC2616 (Hypertext Transfer Protocol -- HTTP/1.1).
Portanto, é fundamental a leitura desse documento, sobretudo da Seção 13 (Caching in HTTP).
Adaptações ou simplificações do padrão podem ser realizadas, desde que devidamente descritas e justificadas na documentação do trabalho.
Todas as questões deixadas em aberto nessa especificação deverão ser definidas por cada grupo e as definições, com eventuais argumentações, deverão fazer parte da documentação.
