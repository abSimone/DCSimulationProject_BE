/* Rimuovere gli auto_increment */

create table pizze (
    ID_pizza int primary key,
    nome varchar(50),
    costo float(3,2)
);

create table ingredienti (
    ID_ingrediente int primary key,
    nome varchar(50)
);

create table pizza_ingrediente (
    FK_pizza int,
    FK_ingrediente int,
    foreign key (FK_pizza) references pizze(ID_pizza),
    foreign key (FK_ingrediente) references ingredienti(ID_ingrediente)
);

commit;

