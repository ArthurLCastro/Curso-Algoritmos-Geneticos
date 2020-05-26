CREATE DATABASE transportadora;

USE transportadora;

CREATE TABLE produtos (
	idproduto int NOT NULL auto_increment,
    nome varchar(50) NOT NULL,
    espaco float NOT NULL,
    valor float NOT NULL,
    quantidade int NOT NULL,
    CONSTRAINT pk_produtos_idproduto PRIMARY KEY (idproduto)
);