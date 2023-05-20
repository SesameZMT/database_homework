# 图书馆管理系统数据库源码

## 表和视图的创建
### 图书信息表创建
其中book_index的设置是为了后续日志视图不出错
```sh
create table book_information (
    book_id NVARCHAR(50) PRIMARY KEY,
    book_name NVARCHAR(50) NOT NULL,
    author NVARCHAR(100) NOT NULL,
    book_category NVARCHAR(50),
    publisher NVARCHAR(50),
    book_is_in INT,
    book_index INT
);
```

### 读者信息表创建
```sh
create table reader_information(
    reader_id NVARCHAR(50) PRIMARY KEY,
    reader_name NVARCHAR(50) NOT NULL,
    reader_class INT NOT NULL,
    reader_borrowednumber INT
);
```

### 图书库存表创建
```sh
create table book_inventory(
book_name NVARCHAR(50) PRIMARY KEY,
book_total int NOT NULL,
book_surplus int NOT NULL
);
```

### 罚款表创建
```sh
create table reader_payment(
    reader_id NVARCHAR(50) PRIMARY KEY,
    reader_name NVARCHAR(50) NOT NULL
);
```

### 借书表创建
```sh
create table reader_borrow(
borrow_book_id NVARCHAR(50),
borrow_bookname NVARCHAR(50) NOT NULL,
borrow_reader_id NVARCHAR(50) NOT NULL,
borrow_book_index INT,
borrow_date DATE
);
```

### 还书表创建
```sh
create table reader_back(
back_book_id NVARCHAR(50),
back_bookname NVARCHAR(50) NOT NULL,
back_reader_id NVARCHAR(50) NOT NULL,
back_book_index INT,
back_date DATE
);
```

### 创建日志视图
```sh
create view history(编号,姓名,借书名称,借书书籍编号,借书日期,还书日期)
as
select reader_borrow.borrow_reader_id,reader_information.reader_name,reader_borrow.borrow_bookname,reader_borrow.borrow_book_id,reader_borrow.borrow_date,reader_back.back_date
from 
reader_borrow,reader_information,reader_back 
where 
borrow_book_id = back_book_id 
and borrow_reader_id = back_reader_id 
and borrow_reader_id = reader_id 
and borrow_book_index=back_book_index;
```

## 触发器的创建
### 创建借书触发器
在借书表上插入后触发<br>
作用：
* 所借书在库存表中馆内现有减一
* 所借书图书信息表中是否在馆内置0
* 借书者总借阅数加一
```sh
delimiter //
create trigger tri_borrow
after insert 
on reader_borrow
for each row
begin
update book_inventory set book_surplus=book_surplus-1 where book_name=new.borrow_bookname;
update book_information set book_is_in=0 where book_id=new.borrow_book_id;
update reader_information set reader_borrowednumber=reader_borrowednumber+1 where reader_id=new.borrow_reader_id;
end //
```

### 创建还书触发器
在还书表上插入后触发<br>
作用：
* 所还书在库存表中馆内现有加一
* 所还书图书信息表中的标记加一
* 所还书图书信息表中是否在馆内置1
```sh
delimiter //
create trigger tri_back
after insert 
on reader_back
for each row
begin
update book_inventory set book_surplus=book_surplus+1 where book_name=new.back_bookname;
update book_information set book_is_in=1 where book_id=new.back_book_id;
update book_information set book_index=book_index+1 where book_id=new.back_book_id;
end //
```

### 创建库存减少触发器
在图书信息表删除后触发<br>
作用：
* 当删除的书籍的名称在库存表中时，总库存和现有库存都减一
* 当总库存为0时直接删除
```sh
delimiter //
create trigger dec_inventory
after delete 
on book_information
for each row
begin
update book_inventory set book_total=book_total-1 where old.book_name in (select a.book_name from (select book_name from book_inventory) a) and old.book_name = book_name;
update book_inventory set book_surplus=book_surplus-1 where old.book_name in (select a.book_name from (select book_name from book_inventory) a) and old.book_name = book_name;
delete from book_inventory where book_total=0;
end //
```

### 创建库存增加触发器
在图书信息表插入后触发<br>
作用：
* 当删除的书籍的名称在库存表中时，总库存和现有库存都加一
* 不在时插入
```sh
delimiter //
create trigger add_inventory
after insert 
on book_information
for each row
begin
update book_inventory set book_total=book_total+1 where new.book_name in (select a.book_name from (select book_name from book_inventory) a);
update book_inventory set book_surplus=book_surplus+1 where new.book_name in (select a.book_name from (select book_name from book_inventory) a);
IF new.book_name not in (select book_name from book_inventory) THEN insert into book_inventory value(new.book_name,1,1);
end IF;
end //
```

## 创建存储过程
### 创建插入还书表的存储过程
```sh
delimiter //
create procedure 
insert_into_readerback(in book_id NVARCHAR(50),in book_name NVARCHAR(50),in reader_id NVARCHAR(50),in back_date date)  
begin 
declare book_index int default 0; 
select book_information.book_index into book_index from book_information where book_information.book_id = book_id; 
insert into reader_back value(book_id,book_name,reader_id,book_index,back_date); 
end //
```

### 创建插入借书表的存储过程
```sh
delimiter //
create procedure 
insert_into_readerborrow(in book_id NVARCHAR(50),in book_name NVARCHAR(50),in reader_id NVARCHAR(50),in back_date date)  
begin 
declare book_index int default 0; 
select book_information.book_index into book_index from book_information where book_information.book_id = book_id; 
insert into reader_borrow value(book_id,book_name,reader_id,book_index,back_date); 
end //
```

### 创建判断是否需要罚款的存储过程
```sh
delimiter //
create procedure ispayment(in book_id NVARCHAR(50),in reader_id NVARCHAR(50))
begin
declare book_index int default 0;
declare borrow_date DATE;
declare back_date DATE;
declare reader_name NVARCHAR(50);
select book_information.book_index into book_index from book_information where book_information.book_id = book_id;
select reader_borrow.borrow_date into borrow_date from reader_borrow where reader_borrow.borrow_book_id=book_id and reader_borrow.borrow_reader_id=reader_id and borrow_book_index=book_index-1;
select reader_back.back_date into back_date from reader_back where reader_back.back_book_id=book_id and reader_back.back_reader_id=reader_id and back_book_index=book_index-1;
IF (select datediff(back_date,borrow_date)) > 7 THEN
select reader_information.reader_name into reader_name from reader_information where reader_information.reader_id = reader_id;
insert into reader_payment value(reader_id,reader_name);
END IF;
end //
```

### 创建删除的存储过程
```sh
delimiter //
create procedure deletereader(in reader_id NVARCHAR(50))
begin
delete from reader_borrow where reader_borrow.borrow_reader_id=reader_id;
delete from reader_back where reader_back.back_reader_id=reader_id;
delete from reader_information where reader_information.reader_id=reader_id;
delete from reader_payment where reader_payment.reader_id=reader_id;
end //
```

### 更新用户的存储过程
```sh
delimiter //
create procedure updatereader(in updatename NVARCHAR(50),in updateid NVARCHAR(50),in user_id NVARCHAR(50))
begin
update reader_information set reader_information.reader_name=updatename where reader_information.reader_id=user_id;
update reader_information set reader_information.reader_id=updateid where reader_information.reader_id=user_id;
update reader_borrow set reader_borrow.borrow_reader_id=updateid where reader_borrow.borrow_reader_id=user_id;
update reader_back set reader_back.back_reader_id=updateid where reader_back.back_reader_id=user_id;
update reader_payment set reader_payment.reader_id=updateid where reader_payment.reader_id=user_id;
end //
```

## 一点测试数据
```sh
insert into book_information value('00000001','测试用书','admin','测试','南开出版社',1,0);
insert into book_information value('00000002','测试用书','admin','测试','南开出版社',1,0);
insert into book_information value('00000003','测试用书','admin','测试','南开出版社',1,0);
```
