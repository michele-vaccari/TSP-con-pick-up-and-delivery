# TSP con pickup and delivery

## Descrizione
A partire dalla base (nodo 0 del grafo) un corriere deve soddisfare n richieste di prelievo e consegna di documenti:
* ogni documento è prelevato in un nodo e consegnato in un altro nodo;
* ogni nodo è riferito a una singola richiesta, ma nel tragitto tra punto di prelievo e consegna si possono prelevare/consegnare altri documenti.

Noto il tempo di percorrenza dei singoli archi, si vuole minimizzare la durata del percorso, con partenza e rientro al deposito.

## Specifiche
Per la risoluzione del problema si sono analizzati sia algoritmi esatti che algoritmi euristici. Nel dettaglio si sono implementati i seguenti algoritmi:
1. Brute Force Enumerator
2. O'Neil - Hoffman Enumerator
3. Greedy Pickup First
4. Greedy Request Order
5. Greedy Nearest Neighbor
6. Greedy Random
7. City Swap
8. City Insert
9. Simulated Annealing
10. Tabu Search
11. Large Neighborhood Search
12. Multi Start Local Search
13. Greedy Randomized Adaptive Search Procedure
14. Greedy Randomized Adaptive Search Procedure with Path Relinking
15. Genetic Algorithm

Gli algoritmi sono sviluppati utilizzando il linguaggio [Python](https://www.python.org/), versione [3.10](https://docs.python.org/3.10/).

## Architettura
L’applicazione è formata da 3 componenti:
- **problem:** è il package che contiene le entità utilizzate per modellare il problema e un generatore di istanze casuali
- **solver:** è il package che contiene gli algoritmi implementati. Utilizza le entità definite nel package problem
- **cli:** è una [Command Line Interface](https://en.wikipedia.org/wiki/Command-line_interface) che consente di generare istanze del problema e testare i vari algoritmi

## Build del sistema

### Prerequisiti
* Python v. 3.10.0 o superiori

### Build/Deploy su Windows
* Creare un ```venv``` nella root del progetto:
    ```bat
    python -m venv venv
    ```
* Attivare il ```venv``` appena creato:
    ```bat
    venv\Scripts\activate.bat
    ```

* Installare le seguenti librerie:
    ```bat
    pip install --force-reinstall -v "click==8.1.3"
    pip install --force-reinstall -v "numpy==1.24.1"
    pip install --force-reinstall -v "pytest==7.2.0"
    pip install --force-reinstall -v "openpyxl==3.0.10"
    pip install --force-reinstall -v "stopwatch==2.0.1"
    ```

## Esempi di utilizzo
Lanciare la [CLI](src/tsppdcli.py) con l'opzione ```--help``` per visualizzare i comandi supportati:
```bat
python tsppdcli.py --help
```
Esempio di output:
```bat
Usage: tsppdcli.py [OPTIONS] COMMAND [ARGS]...

Options:
--help  Show this message and exit.

Commands:
generate-instance  Generates an instance of the tsppd problem.
solve              Solve an instance of the tsppd problem.
```

### Generare una nuova istanza del problema
Lanciare la [CLI](src/tsppdcli.py) con il comando ```generate-instance``` e l'opzione ```--help``` per visualizzare i parametri richiesti:
```bat
python tsppdcli.py generate-instance --help 
Usage: tsppdcli.py generate-instance [OPTIONS]

  Generates an instance of the tsppd problem.

Options:
  --requests INTEGER              Number of requests.
  --weights-as-euclidean-distance / --weights-random
                                  Weights are the Euclidean distance of the
                                  nodes / Weights are randomly generated.
  --output-instance-path TEXT     Path where to save the instance in JSON
                                  format.
  --help                          Show this message and exit.
```

### Risolvere un'istanza del problema utilizzando un particolare algortimo
Lanciare la [CLI](src/tsppdcli.py) con il comando ```solve``` e l'opzione ```--help``` per visualizzare i parametri richiesti:
```bat
python tsppdcli.py solve --help
Usage: tsppdcli.py solve [OPTIONS]

  Solve an instance of the tsppd problem.

Options:
  --input-instance-path TEXT      Path where read the instance in JSON format.
                                  [required]
  --solver-method [brute-force-enumerator|oneil-hoffman-enumerator|greedy-pickup-first|greedy-request-order|greedy-nearest-neighbor|greedy-random|city-swap|city-insert|simulated-annealing|tabu-search|large-neighborhood-search|multi-start-local-search|greedy-randomized-adaptive-search-procedure|greedy-randomized-adaptive-search-procedure-with-path-relinking|genetic-algorithm]
                                  Choose the solver method to use.  [required]
  --help                          Show this message and exit.
```

## Come contribuire al progetto
Se vuoi partecipare allo sviluppo di questo progetto o per ulteriori delucidazioni contattami all'indirizzo: [michele.vaccari@edu.unife.it](mailto:michele.vaccari@edu.unife.it)