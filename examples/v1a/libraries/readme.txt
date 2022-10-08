*********************************************************************
Modelling of SINGLE institutions 
*********************************************************************
pubA.ial : 
- well-commented one. 
- basic one. 
- special service of extending allowance. 
- Settings:
  REGISTRATION:
  - new users need to register and anyone can do that. 
  - allowance for each new user is TWO items. 
  - only registered users can borrow and return books. 
  - normal user = registered user + borrowed books under allowance (non-inertial)
  - available book = in collection + not on loan  (non-inertial)
  BORROW:
  - only register users can generate institional borrowing events. 
  - only normal users are allowed to borrow available books. 
  - borrowed books are obliged to return within the next THREE time instants. 
  - late return issues a fine, and put the user in debt state. 
  - successful borrowing adds loans counter for the user, and changes the state of the borrowed book. 
  RETURN: 
  - returning a book minus loans counter for the user, and changes the state of the borrowed book. 
  EXTEND:
  - new allowance = old allowance + 1 
  INITIAL:
  - book1_a, book2_a, book3_a and book4_a are in the collection and available. 

- Testing in tr1.lp:
  * to run: clingo3 ASPFiles/libA.lp TestTrace/tr1.lp timeline.lp 
  - borrow a book already on loan 
  - borrow more than allowance
  - return in time 
  - borrow a book not in collection 
  - return late 

- To do: 
  - paying fine is not yet implmeneted 
  - loan due clock cannot be cancelled, even though the book has already been returned. 
  
*********************************************************************  
libB.ial (libC.ial):
- extended from pubA.ial
- Settings:
  REGISTRATION:
  - only memeber can register. 
  - external users can only use external registeration. 
  - allowance for each new member user is TWO items, and ONE item for external users. 
  BORROW:
  - external users can only use external borrow.  
  - borrowed books are obliged to return within the next THREE time instants. 
  RETURN: 
  - external return not yet implemented. 
  INITIAL:
  - bob is a member of libB
  - alice is a member of libC 
  - book1_b, book2_b are in collection of libB
  - book1_c, book2_c are in collection of libC 

- Testing in tr2.lp  
  * to run: clingo3 ASPFiles/libB.lp TestTrace/tr2.lp timeline.lp  
  - external users cannot use register
  - external users can only use ext-register
  - external users cannot user borrow 
  - external users can only use ext-borrow
  - external uers can only borrow one item at most.  

- To do:
  - external return is not yet implemented. 

*********************************************************************
Modelling of COORDINATED institutions 
*********************************************************************
pubA.lp, libB.lp and libC.lp 
- pubA responses to all registration requests, but libB/libC only responses to members' requests. 
- external users cannot borrow books from libB/libC. 
- extend events are only recognised by pubA, so null events for libB/libC. 

- Testing in ctr1.lp 
  * to run:  clingo3 timeline.lp TestTrace/ctr1.lp ASPFiles/pubA_c.lp ASPFiles/libB_c.lp ASPFiles/libC_c.lp
   

*********************************************************************
Modelling of INTERACTING institutions 
*********************************************************************
pubA.lp, libB.lp and libC.lp bridge.lp 
- x-generation rules:
    - register with libB for members of libB
         ---gen--> intRegister with libB
         --xgen--> rmRegister for libC -> intRmRegister with libC 
    - rmRequest from libB to libC for members of libB 
         ---gen--> intRmRequest to libB
         --xgen--> rmBorrow for libC -> intBorrow for libC
    - same rules for libC to generate events for libB
- x-consequence rules: 
    - issueFine by libB --xinit--> inDebt of libC
    - issueFine by libC --xinit--> inDebt of libB

- Testing in ctr2.lp 
  * to complie: python main_br_all.py -il ../InstALFiles/libC.ial ../InstALFiles/libB.ial ../InstALFiles/pubA.ial -d ../DomainFiles/domain.idc -bd ../DomainFiles/domain_bridge.idc -b ../InstALFiles/bridge.ial  -m c -o ../ASPFiles
  * to run: clingo3 timeline.lp TestTrace/ctr2.lp ASPFiles/pubA.lp ASPFiles/libB.lp ASPFiles/libC.lp ASPFiles/bridge.lp  > Result/ctr2.res


*********************************************************************
Modelling of MERGED institutions 
*********************************************************************
pubA.lp, libB.lp and libB.lp bridge.lp  ===> mlib.lp 

Merging fluents: 
- TypeA: max-overrides merging. for example, 
    pubA: allowance(bob, 2) 
    libB: allowance(bob, 2)
    libC: allowance(bob, 1)
    ===> after merge, we could give allowance(bob, 2). 

- TypeB: presence-overrides merging. for example,
    pubA: inDebt(bob) 
    libB: 
    libC: 
    ===> after merge, we should have inDebt(bob). 

- TypeC: add-up merging. for example,
    pubA: loans(bob, 1). 
    libB: loans(bob, 1). 
    libC: loans(bob, 0). 
    ===> after merge, we should have loans(bob, 2). 


**** To do 
- poster first 
- send emails to organizor






