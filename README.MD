Universidade Federal do Rio de Janeiro <br>
PROJETO DE CIRCUITOS ELÉTRICOS 2 <br>
Gabriel de Lima Moura - 118045099 <br>


FORMATO DAS ENTRADAS: <br>

Resistor:       R< name >  < n+ >  < n- > <resistance>
  
VCCS:           G< name >  < io+ > < io- > <vi+> <vi-> <transconductance>
    
VCVC:           E< name > < vo+ >  < vo- > <vi+> <vi-> <gain>
    
CCCS:           F< name > < io+ > <io-> <ii+> <ii-> <gain>
    
CCVS:           H< name > < vo+ > < vo- > < ii+ > < ii- > <transresistance>
    
Fonte I:        I< name > < io+ > < io- > < type >
  
  opções:                         
    
    <DC> <current>
    
    <sin> <IO> <IA> <FREQ> <TD> <THETA> <PHASE> -> ex.: I(t)=IO+IA⋅exp[−THETA⋅(t−TD)]⋅sin[2πFREQ(t−TD)+(PHASE/360)]

Fonte V:        V< name > < vo+ > < vo- > < type >
   
   opções:                        
     
     <DC> <voltage>
      
     <sin> <VO> <VA> <FREQ> <TD> <THETA> <PHASE> -> ex.: V(t)=VO+VA⋅exp[−THETA⋅(t−TD)]⋅sin[2πFREQ(t−TD)+(PHASE/360)]

Capacitor:      C< name > < n+ > < n- > < capacitance >  [< InitialVoltage >]
    
Indutor:        L< name > < n+ > < n- > < Inductance >  [< InitialCurrent >]
    
Transformador ideal: K< name > < n1+ > < n1- > < n2+ > < n2- > < relação de espiras >
    
<br> <br>

Como usar: 

    . Digite a netlist do circuito no arquivo data.txt 
    . execute o arquivo run.py
    . Os resultados serão escritos no arquivo results.txt

<br>
Pacotes/Bibliotecas necessárias : 

    . numpy
                                    
