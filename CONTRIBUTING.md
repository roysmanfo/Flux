# Contributing
Se leggi questo file, vuol dire che sei interessato/a al progetto, il che mi fa piacere.  
In questo file troverai alcune istruzioni e consiigli per iniziare a lavorare a __Cristal__: da cosa installare nel sistema, a come suggerire le tue modifiche su GitHub

## Setup

Per cominciare devi sapere che Cristal è scritto in Python, quindi assicurati di avecelo insallato sul tuo dispositivo direttamente
dal [sito uffuciale](https://https://www.python.org/downloads/). Assicurati che la versione sia almeno __3.7__ o superiore (Attualmente Cristal usa la __3.9.6__) 
Per controllare che versione stai usando apri il termiale e scrivi il seguente comando:
```
python --version
```
  
### Librerie
Per lo sviluppo di diverse funzionalità si è ricorso all'utilizzo di librerie per questioni di efficienza.  
Per cominciare l'installazione delle librerie, apri il terminale ed esegui i seguenti comandi:
- __Colorama__:  
  Serve a colorare il testo sul terminale.  
  L'installazione : comando `pip install colorama`  
- __gTTS__(Google Text To Speech):
  Serve a converire il l'imput testuale dell'utente in un file audio
  Installazione: comando `pip install gTTS`
- __watchdog__:
  Tra le cose che fà può anche controllare cambiamenti nelle directory, questo verrà usato per un comando futuro
  Installazione: comando `pip install watchdog`