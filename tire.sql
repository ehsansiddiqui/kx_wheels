--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: kx_tirebrandimagesthumbnail; Type: TABLE; Schema: public; Owner: kxwheels; Tablespace: 
--

CREATE TABLE kx_tirebrandimagesthumbnail (
    id integer NOT NULL,
    brand_name character varying(155) NOT NULL,
    size character varying(50) NOT NULL,
    path character varying(1000) NOT NULL
);


ALTER TABLE public.kx_tirebrandimagesthumbnail OWNER TO kxwheels;

--
-- Name: kx_tirebrandimagesthumbnail_id_seq; Type: SEQUENCE; Schema: public; Owner: kxwheels
--

CREATE SEQUENCE kx_tirebrandimagesthumbnail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kx_tirebrandimagesthumbnail_id_seq OWNER TO kxwheels;

--
-- Name: kx_tirebrandimagesthumbnail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kxwheels
--

ALTER SEQUENCE kx_tirebrandimagesthumbnail_id_seq OWNED BY kx_tirebrandimagesthumbnail.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kxwheels
--

ALTER TABLE ONLY kx_tirebrandimagesthumbnail ALTER COLUMN id SET DEFAULT nextval('kx_tirebrandimagesthumbnail_id_seq'::regclass);


--
-- Data for Name: kx_tirebrandimagesthumbnail; Type: TABLE DATA; Schema: public; Owner: kxwheels
--

COPY kx_tirebrandimagesthumbnail (id, brand_name, size, path) FROM stdin;
11	Kumho™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/2f/64/2f641b4e10cd7ebdbe9377d972ee5adf.jpg
21	13 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/35/24/35241b6fd4e7b2ff3b7f3e93bc865682.jpg
25	14 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/f4/6a/f46a879d4815bcc5146db78c113a1c38.jpg
28	15 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/e1/ff/e1ff24f5780fd0cc4215703d88460190.jpg
22	16 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/4c/63/4c635ef5f4793277c1e627447a0e2353.jpg
24	17 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/c3/fd/c3fd9eb0fe3e3c71097aa944abd1f530.jpg
23	18 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/bc/31/bc31a97260786c8eb1f5f1e456eaf9a2.jpg
20	19 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/ed/88/ed8847cfb6653195d824683d56610832.jpg
15	20 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/a1/57/a1577823acb4f0d50a30bcdae77c5771.jpg
26	21 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/0e/c5/0ec5e38cf38aa29e9e52fcfb1d18ed75.jpg
16	22 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/3a/fa/3afa9a446059b2dfa8689872c06816de.jpg
17	24 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/03/14/0314f4c204c5e8e4bba119424ce7794e.jpg
18	26 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/52/95/5295d69728058528ff1ae8db0c01a388.jpg
19	28 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/9d/c5/9dc5c97475e097124006ceff2a4f5573.jpg
27	30 Inch Tire Specials	med	https://kxwheels.s3.amazonaws.com/cache/76/55/76553ef5700b81b4f8f5cf45c479a6c4.jpg
2	Achilles™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/03/37/0337f85d85790d61d80135f418b133f4.jpg
7	Atturo™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/41/62/4162d63c900155a6809a90eaee5d74ca.jpg
42	BFGoodrich™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/c7/28/c728a4219d4c79b0ba0623cf4f2c15d6.jpg
31	Bridgestone™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/cb/ac/cbaccb056c28e5508581f7449c31d398.jpg
38	Continental™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/91/4f/914f059ff191c1fb8cc65a40bebca682.jpg
1	Cooper™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/b6/4a/b64ad069eaebcb5967442d8771c269ce.jpg
30	Dick Cepek™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/04/1e/041e1b31b08481eeab4801895ea209bc.jpg
39	Dunlop™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/6a/a0/6aa08149f9de7019412333d56f2a5a28.jpg
32	EverGreen™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/89/cd/89cdf083adc7a878f20ea21bafb46cc9.jpg
3	Falken™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/8c/64/8c640fc150fc24bc4465191662cfec25.jpg
4	Federal™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/bb/ce/bbce41b831a203ed4695f8d958aa6511.jpg
37	Firestone™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/d0/ab/d0abd1ca68a1a121a3a9cbd94e590d8a.jpg
8	Fullway™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/85/c1/85c1293216c0e7153b9ffe52f2f55a78.jpg
36	General™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/ee/94/ee94c49491d1a756641f1a298f7a7a34.jpg
41	Goodyear™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/32/8c/328c22a4569d883bd73cfe8607dbb9be.jpg
34	Hankook™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/fa/b1/fab104e0d1dbed71e64fef0d53983829.jpg
43	Infinity™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/84/42/844225b702723a0a9ed84c91b6c384f5.jpg
9	Lexani™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/f7/c4/f7c49f3f0ec6293e3f6ea1cafd82ccc4.jpg
10	Lionhart™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/42/cd/42cd714e40e251924e67cfccf9884f0e.jpg
35	Michelin™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/9b/a0/9ba0db665d47d9b54731b89023f88db6.jpg
29	Mickey Thompson™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/25/a8/25a8204fdf757b79e22862832918976c.jpg
5	Nexen™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/28/cd/28cd996411d2323ce1ce3b36f66e7c8c.jpg
12	Nitto™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/21/aa/21aa17908f8d08fbf8e1353b84e9de34.jpg
40	Pirelli™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/c9/73/c97353fd83c223c5114f9f79d97a3d44.jpg
13	Procomp Tires	med	https://kxwheels.s3.amazonaws.com/cache/7d/07/7d07076f4fce549a8a20883e87854c91.jpg
44	Roadstone™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/04/ea/04eaaa71c6f2d5907babb97bfaa5c4ce.jpg
45	Sumo™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/d5/81/d581931023bc637d3e0800e9473ac373.jpg
33	Sunny™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/29/fe/29fea38d9bf6daf2187e271718aec0a9.jpg
6	Toyo™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/92/03/9203cdd8750d5ed25f4687dea96ecdd5.jpg
46	Wanli™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/73/85/7385e308aee07f6ef08c6288cfc3b3b3.jpg
14	Yokohama™ Tires	med	https://kxwheels.s3.amazonaws.com/cache/1f/1b/1f1bde6c6572bc2375c0de700ffa3004.jpg
\.


--
-- Name: kx_tirebrandimagesthumbnail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kxwheels
--

SELECT pg_catalog.setval('kx_tirebrandimagesthumbnail_id_seq', 1, false);


--
-- Name: kx_tirebrandimagesthumbnail_pkey; Type: CONSTRAINT; Schema: public; Owner: kxwheels; Tablespace: 
--

ALTER TABLE ONLY kx_tirebrandimagesthumbnail
    ADD CONSTRAINT kx_tirebrandimagesthumbnail_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

