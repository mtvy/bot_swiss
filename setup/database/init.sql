
CREATE TABLE message_tb(
    id serial primary key, 
    user_id varchar(15), 
    oper_id varchar(15), 
    date_start VARCHAR(255), 
    text TEXT, 
    status VARCHAR(255)
);

CREATE TABLE feedback_tb(
    id serial primary key, 
    oper_id varchar(15),
    user_id varchar(15),
    date_enter varchar(255), 
    text_fb text,
    status varchar(255)
);

CREATE TABLE collection_tb(
    id               serial primary key, 
    admin_id         VARCHAR(128), 
    cashier_id       VARCHAR(128), 
    office           VARCHAR(128), 
    terminal_number  TEXT, 
    cash             TEXT, 
    cash_return_info TEXT, 
    doc_number       TEXT, 
    PCR              TEXT, 
    PCR_express      TEXT, 
    analyzes_count   TEXT, 
    comment          TEXT, 
    admin_date       VARCHAR(128), 
    cashier_date     VARCHAR(128), 
    status           VARCHAR(128) 
);

CREATE TABLE messageId_tb(
    message_id INTEGER
);

INSERT INTO messageId_tb (message_id) VALUES (403);

CREATE TABLE account_tb(
    id            serial primary key,
    telegram_id   varchar(255), 
    login         varchar(255), 
    name          varchar(255), 
    oper_ids      varchar(10)[], 
    conversation  varchar(255), 
    discount      varchar(255), 
    tags          varchar(10)[], 
    ref           varchar(255), 
    personal_data varchar(255), 
    language      varchar(255), 
    feedback_st   varchar(255), 
    timer_conv    integer,
    link_enter    VARCHAR(64)        
); 
