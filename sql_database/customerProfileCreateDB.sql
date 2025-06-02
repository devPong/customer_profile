create database customer_profile;

CREATE TABLE "gender" (
  "id" serial PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "person" (
  "id" serial PRIMARY KEY,
  "active" bool,
  "preName" varchar,
  "firstName" varchar,
  "lastName" varchar,
  "nickName" varchar,
  "gender_id" int,
  "brithday" date,
  "address" text,
  "subdistrict_id" int,
  "district_id" int,
  "province_id" int,
  "postcode" varchar,
  "mobile" varchar,
  "facebook" varchar,
  "line_id" varchar,
  "instagram" varchar,
  "tictok" varchar,
  "hobby" text,
  "food_favorite" text,
  "food_allergies" text,
  "alcohol" text,
  "wine" text,
  "cigarettes" text,
  "create_uid" int,
  "create_date" timestamp,
  "write_uid" int,
  "write_date" timestamp
);

CREATE TABLE "m2m_person_relation" (
  "main_person_id" int,
  "sub_person_id" int,
  "relation_type_id" int
);

CREATE TABLE "person_relation_type" (
  "id" serial PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "person_shop_relation_type" (
  "id" serial PRIMARY KEY,
  "name" int
);

CREATE TABLE "m2m_person_shop" (
  "type_id" int,
  "shop_id" int,
  "person_id" int
);

CREATE TABLE "shop_type" (
  "id" serial PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "shop_relation_type" (
  "id" serial PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "shop" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "active" bool,
  "type" int,
  "address" text,
  "subdistrict_id" int,
  "district_id" int,
  "province_id" int,
  "postcode" varchar,
  "phone" varchar,
  "fax" varchar,
  "mobile" varchar,
  "erp_id" int,
  "car_sale_monthly_avg" decimal,
  "films_use_year_avg" decimal,
  "car_use_year_avg" decimal,
  "shipping" text,
  "shipping_erp_id" int,
  "credit_amount" decimal,
  "credit_term" decimal,
  "create_uid" int,
  "create_date" timestamp,
  "write_uid" int,
  "write_date" timestamp
);

CREATE TABLE "m2m_shop_relation" (
  "shop_master_id" int,
  "shop_sub_id" int,
  "type_id" int
);

CREATE TABLE "province" (
  "id" serial PRIMARY KEY,
  "name" varchar
);

CREATE TABLE "district" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "province_id" int
);

CREATE TABLE "subdistrict" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "post_code" varchar,
  "district_id" int
);

CREATE TABLE "sys_user" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "erp_uid" int,
  "type" varchar,
  "active" bool
);

CREATE TABLE "sys_method" (
  "id" serial PRIMARY KEY,
  "name" varchar,
  "active" bool
);

CREATE TABLE "sys_permission" (
  "id" serial PRIMARY KEY,
  "user_id" int,
  "method_id" int
);

CREATE TABLE "sys_log" (
  "id" serial PRIMARY KEY,
  "date" timestamp,
  "action" text,
  "user_id" int
);

CREATE TABLE "attachFiles" (
  "id" serial PRIMARY KEY,
  "date" timestamp,
  "file_type" varchar,
  "path_file" varchar,
  "relate_type" varchar,
  "relate_id" int,
  "active" bool
);

ALTER TABLE "district" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("id");

ALTER TABLE "subdistrict" ADD FOREIGN KEY ("district_id") REFERENCES "district" ("id");

ALTER TABLE "shop" ADD FOREIGN KEY ("type") REFERENCES "shop_type" ("id");

ALTER TABLE "shop" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("id");

ALTER TABLE "shop" ADD FOREIGN KEY ("district_id") REFERENCES "district" ("id");

ALTER TABLE "shop" ADD FOREIGN KEY ("subdistrict_id") REFERENCES "subdistrict" ("id");

ALTER TABLE "person" ADD FOREIGN KEY ("province_id") REFERENCES "province" ("id");

ALTER TABLE "person" ADD FOREIGN KEY ("district_id") REFERENCES "district" ("id");

ALTER TABLE "person" ADD FOREIGN KEY ("subdistrict_id") REFERENCES "subdistrict" ("id");

ALTER TABLE "person" ADD FOREIGN KEY ("gender_id") REFERENCES "gender" ("id");

ALTER TABLE "m2m_person_relation" ADD FOREIGN KEY ("main_person_id") REFERENCES "person" ("id");

ALTER TABLE "m2m_person_relation" ADD FOREIGN KEY ("sub_person_id") REFERENCES "person" ("id");

ALTER TABLE "m2m_person_relation" ADD FOREIGN KEY ("relation_type_id") REFERENCES "person_relation_type" ("id");

ALTER TABLE "person" ADD FOREIGN KEY ("create_uid") REFERENCES "sys_user" ("id");

ALTER TABLE "person" ADD FOREIGN KEY ("write_uid") REFERENCES "sys_user" ("id");

ALTER TABLE "m2m_person_shop" ADD FOREIGN KEY ("person_id") REFERENCES "person" ("id");

ALTER TABLE "m2m_person_shop" ADD FOREIGN KEY ("shop_id") REFERENCES "shop" ("id");

ALTER TABLE "m2m_person_shop" ADD FOREIGN KEY ("type_id") REFERENCES "person_shop_relation_type" ("id");

ALTER TABLE "shop" ADD FOREIGN KEY ("create_uid") REFERENCES "sys_user" ("id");

ALTER TABLE "shop" ADD FOREIGN KEY ("write_uid") REFERENCES "sys_user" ("id");

ALTER TABLE "m2m_shop_relation" ADD FOREIGN KEY ("shop_master_id") REFERENCES "shop" ("id");

ALTER TABLE "m2m_shop_relation" ADD FOREIGN KEY ("shop_sub_id") REFERENCES "shop" ("id");

ALTER TABLE "m2m_shop_relation" ADD FOREIGN KEY ("type_id") REFERENCES "shop_relation_type" ("id");

ALTER TABLE "sys_permission" ADD FOREIGN KEY ("user_id") REFERENCES "sys_user" ("id");

ALTER TABLE "sys_permission" ADD FOREIGN KEY ("method_id") REFERENCES "sys_method" ("id");

ALTER TABLE "sys_log" ADD FOREIGN KEY ("user_id") REFERENCES "sys_user" ("id");
