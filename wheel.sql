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
-- Name: kx_wheelbrandimagesthumbnail; Type: TABLE; Schema: public; Owner: kxwheels; Tablespace: 
--

CREATE TABLE kx_wheelbrandimagesthumbnail (
    id integer NOT NULL,
    brand_name character varying(155) NOT NULL,
    size character varying(50) NOT NULL,
    path character varying(1000) NOT NULL
);


ALTER TABLE public.kx_wheelbrandimagesthumbnail OWNER TO kxwheels;

--
-- Name: kx_wheelbrandimagesthumbnail_id_seq; Type: SEQUENCE; Schema: public; Owner: kxwheels
--

CREATE SEQUENCE kx_wheelbrandimagesthumbnail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kx_wheelbrandimagesthumbnail_id_seq OWNER TO kxwheels;

--
-- Name: kx_wheelbrandimagesthumbnail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kxwheels
--

ALTER SEQUENCE kx_wheelbrandimagesthumbnail_id_seq OWNED BY kx_wheelbrandimagesthumbnail.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: kxwheels
--

ALTER TABLE ONLY kx_wheelbrandimagesthumbnail ALTER COLUMN id SET DEFAULT nextval('kx_wheelbrandimagesthumbnail_id_seq'::regclass);


--
-- Data for Name: kx_wheelbrandimagesthumbnail; Type: TABLE DATA; Schema: public; Owner: kxwheels
--

COPY kx_wheelbrandimagesthumbnail (id, brand_name, size, path) FROM stdin;
72	Status Wheels	med	https://kxwheels.s3.amazonaws.com/cache/17/93/17935762374b7a9863925077b62f52d7.jpg
2	Blaque Diamond Wheels	med	https://kxwheels.s3.amazonaws.com/cache/38/9f/389f3e61f17535ad5db4fb23a75fdf5b.jpg
24	MKW Wheels	med	https://kxwheels.s3.amazonaws.com/cache/00/e5/00e5d238bfaf0b2eacea83f29dd9ff6c.jpg
28	Foose Wheelss	med	https://kxwheels.s3.amazonaws.com/cache/f0/cb/f0cb2f9bd5ac0032fc5b680c703d0278.jpg
86	G-FX Wheels	med	https://kxwheels.s3.amazonaws.com/cache/41/c4/41c4d0bc04a9da1d070935ff0fcda07f.jpg
1	Maas  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/74/0f/740fd40d7820aa5905270fbe7f531af7.jpg
59	Styluz Wheels	med	no image
97	2 Crave  Extreme Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a8/c8/a8c86a42126fdb4e9ee5fdbebec1164d.jpg
84	2 Crave  SF-1 Wheels	med	https://kxwheels.s3.amazonaws.com/cache/45/be/45be64c46a9d63df84d6faa635a937ad.jpg
32	US Mags	med	https://kxwheels.s3.amazonaws.com/cache/2b/44/2b44397f7d7b814fc22249b0916d31c0.jpg
89	LRG Rims	med	https://kxwheels.s3.amazonaws.com/cache/9f/52/9f52d25696716f300920cc778a9a2fc7.jpg
99	OE CREATIONS	med	https://kxwheels.s3.amazonaws.com/cache/bc/50/bc50e03b392b47f44556c91332629734.jpg
103	Ice Metal Winter Wheels	med	https://kxwheels.s3.amazonaws.com/cache/95/5d/955d8456070423abfc897019a01c9d11.jpg
37	Noir Wheels	med	https://kxwheels.s3.amazonaws.com/cache/c9/fc/c9fc91b9c45945e3ce842ed35bd6a10b.jpg
105	ROCKSTAR BY KMC WHEELS	med	https://kxwheels.s3.amazonaws.com/cache/c1/28/c12837f50b94026a631b693325947ea0.jpg
109	American Racing ATX  Offroad Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/eb/4a/eb4af99f1457ab6c9d0c8cc4992530e1.jpg
88	B/G Rod Works Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2d/0a/2d0a0a81b01f2d2553594c6e68f78988.jpg
64	Dick Cepek Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e3/16/e31696cb9f719ab45bfe4cf713f4d2be.jpg
92	22 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/3a/fa/3afa9a446059b2dfa8689872c06816de.jpg
4	Drifz Racing Wheels	med	https://kxwheels.s3.amazonaws.com/cache/ec/65/ec65a5ebf57ef57439af8a7e4f8d1335.jpg
11	Merceli Wheels	med	https://kxwheels.s3.amazonaws.com/cache/47/04/47041ffbdc9d6509408cd549847d3ffa.jpg
7	Katana Wheels	med	https://kxwheels.s3.amazonaws.com/cache/89/b1/89b11416cfad52f04256273e84d191aa.jpg
41	Incubus Wheels	med	https://kxwheels.s3.amazonaws.com/cache/30/39/3039c6bc552d316c98a95d982446d821.jpg
67	CEC Wheels	med	https://kxwheels.s3.amazonaws.com/cache/5f/65/5f659be9955beb5f591ff67f5597a79d.jgp
6	Katana Extreme Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/89/b1/89b11416cfad52f04256273e84d191aa.jpg
16	Strada Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e2/8f/e28f0e7adda4913668729bca7e93bdd8.jpg
20	GFG Supremo Forged Wheels	med	https://kxwheels.s3.amazonaws.com/cache/fd/7b/fd7bd239e148f4336b8804316255dcdd.jpg
46	V-Rock Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/8e/82/8e82abd1d8701b90214f5f274ed071c3.jpg
50	Versante Wheels	med	https://kxwheels.s3.amazonaws.com/cache/3c/03/3c03a4e915cb1a471defab694541c466.jpg
53	Vision Wheels	med	https://kxwheels.s3.amazonaws.com/cache/0e/0a/0e0ab6ad6b94719dea0942a12df84119.jpg
70	XXR Wheels	med	https://kxwheels.s3.amazonaws.com/cache/99/6e/996eef80d453530ca87fab2ca8dba960.jpg
143	Mickey Thompson Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e4/77/e47708824443ef13caecc67b172d52f8.jpg
146	OE Performance Wheels	med	https://kxwheels.s3.amazonaws.com/cache/12/ee/12eec4901099a55411fa72cdccf25b8a.jpg
152	Ultra Wheels	med	https://kxwheels.s3.amazonaws.com/cache/3d/ea/3dea08564218529b00ea24116d76c7c5.jpg
15	Scorpion Offroad Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/43/3f/433f3c665630ae4bee1e35df7ae9fbcc.jpg
156	Konig  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/db/41/db419e3f515924cdc9e6ab8a46a964a4.jpg
17	Giovanna  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/97/c5/97c5412a230771336054144e33c5235f.jpg
131	Bravado Wheels	med	https://kxwheels.s3.amazonaws.com/cache/30/1c/301c26d2f44365c574d3735f75467af8.jpg
155	Cali Offroad Wheels	med	https://kxwheels.s3.amazonaws.com/cache/36/95/36956701545905d6af2cdfd84f627b5e.jpg
135	Devino Wheels	med	https://kxwheels.s3.amazonaws.com/cache/40/f4/40f4a19ec721ed1ba67ede76958e568d.jpg
26	Eagle Alloy Wheels	med	https://kxwheels.s3.amazonaws.com/cache/4d/a0/4da04c8250b329b563e3cab303e5a33e.jpg
128	Enkei Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2a/93/2a93bf0472c58d7ec82b0bd168407ac6.jpg
5	Envy Wheels	med	https://kxwheels.s3.amazonaws.com/cache/3b/b7/3bb72e5a7bbed302202b83541487cb6d.jpg
10	Kyowa Racing Wheels	med	https://kxwheels.s3.amazonaws.com/cache/7e/c3/7ec3270853668960119906daed7d2daf.jpg
25	MKW Offroad Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e2/76/e2762ba32373c3506880eedc480e297a.jpg
18	Gianelle  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/54/79/547990a5785d5b3cdd369c6ed46de323.jpg
27	Foose Classics Hot Rod Series	med	https://kxwheels.s3.amazonaws.com/cache/f2/c0/f2c01781061e84aa1d16def979792a15.jpg
29	Niche Wheels Sport Series	med	https://kxwheels.s3.amazonaws.com/cache/03/5c/035cf75e511ca80a7696309f0d80cdf5.jpg
30	Niche  Wheels Tour Series	med	https://kxwheels.s3.amazonaws.com/cache/5d/17/5d1721787d31605a09e3699644b8c537.jpg
31	Niche  Wheels Track Series	med	https://kxwheels.s3.amazonaws.com/cache/5d/17/5d1721787d31605a09e3699644b8c537.jpg
19	Koko Kuture  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/80/4e/804eeb13915bd961c1148c6b5738838a.jpg
12	Mystikol Wheels	med	https://kxwheels.s3.amazonaws.com/cache/10/42/1042ce8b81adf79010a432e3913744ba.jpg
33	MRR Wheels	med	https://kxwheels.s3.amazonaws.com/cache/6e/0e/6e0e1d796c7b9d8e0fd162ff38301626.jpg
23	Avenue Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e5/0a/e50ac132ef0dd0fb812d43045ff2d277.jpg
9	Ninja Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2c/f2/2cf2819d57438ff51885cb85f5fdd170.jpg
13	Gitano Wheels	med	https://kxwheels.s3.amazonaws.com/cache/58/34/5834dd3b5b7d8a188530c56087fb91f7.jpg
14	VCT Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a3/57/a35778e7e3455010cf52f07604bf3eb0.jpg
21	Hipnotic Wheels | Hipnotic Rims	med	https://kxwheels.s3.amazonaws.com/cache/99/64/996482bea3ed6384cf96719d17a016ef.jpg
22	Lexani Wheels	med	https://kxwheels.s3.amazonaws.com/cache/5a/8f/5a8f01f29b541a57bb5f2f89ee614691.jpg
34	Roderick Wheels	med	https://kxwheels.s3.amazonaws.com/cache/82/7c/827c900b9d7a9009fd4a2ff039b80d5a.jpg
36	Performance Replica Wheels	med	https://kxwheels.s3.amazonaws.com/cache/0f/ea/0fea51f5c6bcc0725bf4906083128a73.jpg
125	Raceline Wheels	med	https://kxwheels.s3.amazonaws.com/cache/fe/4f/fe4fe87d7d195e17ebfc8cc228815bee.jpg
62	16 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/4c/63/4c635ef5f4793277c1e627447a0e2353.jpg
60	18 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/bc/31/bc31a97260786c8eb1f5f1e456eaf9a2.jpg
57	19 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/ed/88/ed8847cfb6653195d824683d56610832.jpg
90	20 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/a1/57/a1577823acb4f0d50a30bcdae77c5771.jpg
132	21 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/23/df/23df652cd8485cd8bc654a46632bf7ef.jpg
91	24 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/03/14/0314f4c204c5e8e4bba119424ce7794e.jpg
63	28 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/9d/c5/9dc5c97475e097124006ceff2a4f5573.jpg
82	2 Crave  Black Diamond Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2a/07/2a078402c4ee9538eaba31fa1eda5e61.jpg
83	2 Crave  Fiero Wheels	med	https://kxwheels.s3.amazonaws.com/cache/c2/ac/c2acd0c85e6793917a9903a624d5a244.jpg
96	2 Crave  Heavy Hitters Wheels	med	https://kxwheels.s3.amazonaws.com/cache/16/c1/16c197a009cb6431ba70969cc19458b9.jpg
101	Adventus Wheels	med	https://kxwheels.s3.amazonaws.com/cache/44/4d/444d90383565cf64c1a23699003cdfe5.jpg
38	Akuza Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a7/f3/a7f389b092fe24e622457d15c6baa9d0.jpg
129	American Eagle Hardrock Series	med	https://kxwheels.s3.amazonaws.com/cache/2f/92/2f9243377cf2be91c9e2649eb3441f35.jpg
108	American Racing Forged Wheels	med	https://kxwheels.s3.amazonaws.com/cache/94/6c/946c4e566d2b043ab0d12cc8c9f01cf4.jpg
107	American Racing Wheels	med	https://kxwheels.s3.amazonaws.com/cache/94/6c/946c4e566d2b043ab0d12cc8c9f01cf4.jpg
35	Fathom Designs Wheels	med	https://kxwheels.s3.amazonaws.com/cache/1d/c0/1dc081ecd0c2c636fc95cb59ea74a2fc.jpg
42	Menzari Wheels	med	https://kxwheels.s3.amazonaws.com/cache/81/64/8164137093c443bab06fcf4d5115b4be.jpg
43	Procomp Wheels	med	https://kxwheels.s3.amazonaws.com/cache/fe/34/fe345321b946737f42b4f4a8fd1cd5b6.jpg
44	RBP Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e7/67/e767c35a3058a570fa84769391ea287a.jpg
45	Verde Wheels	med	https://kxwheels.s3.amazonaws.com/cache/c8/bd/c8bdfa233714db89f2f9598bb39622f5.jpg
48	Verde Replica Wheels	med	https://kxwheels.s3.amazonaws.com/cache/c7/7e/c77eb4234d942145653ce4dfd40f5ecf.jpg
51	Forza Wheels	med	https://kxwheels.s3.amazonaws.com/cache/cd/c1/cdc15c553db6c41d563b593c8dd07e3e.jpg
115	Fuel Offroad Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2a/4e/2a4e33dd5ae4d5b93df47e7742715686.jpg
58	15 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/e1/ff/e1ff24f5780fd0cc4215703d88460190.jpg
95	2 Crave  Mach Wheels	med	https://kxwheels.s3.amazonaws.com/cache/68/2f/682fecb964d54b9491789601caa12d23.jpg
93	26 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/52/95/5295d69728058528ff1ae8db0c01a388.jpg
81	2 Crave  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/14/22/1422871b25d31c2f5781e003dfffcb87.jgp
68	Advanti Racing Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e8/cd/e8cd8e63435606d661115b30531963df.jpg
100	Asanti Black Label Wheels	med	https://kxwheels.s3.amazonaws.com/cache/29/de/29de7d5c2c6e5b68d978f02b8c2fa301.jpg
39	Ballistic Offroad Wheels	med	https://kxwheels.s3.amazonaws.com/cache/f8/35/f835416ae86835ca195c939d675cccee.jpg
49	Euro Tek Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e4/47/e447ffbfe26c95c087cbc47c8841d375.jgp
127	MIRO Wheels	med	https://kxwheels.s3.amazonaws.com/cache/f6/7e/f67e6688340c8a26d0184928770a4988.jpg
123	Carlisle  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/01/ee/01eecb1c6223393c66cb661954e72d6d.jpg
102	Centerline Wheels 	med	https://kxwheels.s3.amazonaws.com/cache/7c/55/7c554b0b680bf77aa995865de8cae748.jpg
3	Cragar Wheels	med	https://kxwheels.s3.amazonaws.com/cache/88/7c/887cf1fc3d0c4f2ee3a74058fcb228b3.jpg
130	BOSS Motorsports Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a1/fd/a1fd91e45c51067203e10c90960c9804.jpg
79	Cruiser Alloy Wheels	med	https://kxwheels.s3.amazonaws.com/cache/78/8b/788b7e932b45cf50be8536465b119448.jpg
134	Deegan 38 Wheels	med	https://kxwheels.s3.amazonaws.com/cache/ce/af/ceaf5036869b3af799c63556120eb38a.jpg
40	Diablo Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e5/07/e507529d483e09f93f9224b6f4e15f17.jpg
124	Dolce Wheels	med	https://kxwheels.s3.amazonaws.com/cache/95/a2/95a2940d35f956622c6d9701f01aa29e.jpg
8	Drag Concepts Wheels	med	https://kxwheels.s3.amazonaws.com/cache/e7/7e/e77e115692bc76a03a5d307dd8d09d65.jpg
77	Drag Tuner Car Wheels	med	https://kxwheels.s3.amazonaws.com/cache/bf/cd/bfcd1d9bc9311c3c0e9691d963759be3.jpg
75	Focal Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2f/97/2f972ed24c05a2af42f008f40387082d.jpg
85	Hostile Offroad Wheels	med	https://kxwheels.s3.amazonaws.com/cache/99/92/999261e5f7e945c3ddbf0b5686af8c3a.jpg
139	Fondmetal	med	https://kxwheels.s3.amazonaws.com/cache/c2/d1/c2d1252e3f2d6edf9927de0fdae1116c.jpg
55	Milanni Wheels	med	https://kxwheels.s3.amazonaws.com/cache/ae/3f/ae3fcd41e80b37dfee8d9d23fe654167.jpg
98	Method Race Wheels	med	https://kxwheels.s3.amazonaws.com/cache/47/f7/47f7f5446025708e90ec391e7b37595f.jpg
110	Helo Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a2/dd/a2ddca3b82f920e5725c12f1b744f2b9.jpg
111	KMC Wheels	med	https://kxwheels.s3.amazonaws.com/cache/51/20/512091b1ce2cbafff4a5449fd683b32e.jpg
117	Ion Alloy Wheels	med	https://kxwheels.s3.amazonaws.com/cache/8e/ca/8ecad9a80d80fcbb0a02772cd1685e5c.jpg
141	Gear Alloy Offroad Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/63/1e/631ebb24d5f70e669c4c96a133cd62fc.jpg
142	ICW Racing  Wheels	med	https://kxwheels.s3.amazonaws.com/cache/db/6e/db6e7ce87215ed3292d7d339b9025e5b.jpg
157	Maxxim Wheels	med	https://kxwheels.s3.amazonaws.com/cache/06/c4/06c4020332397b5fa9e995c8671e00b5.jpg
159	MAMBA Wheels	med	https://kxwheels.s3.amazonaws.com/cache/4b/7a/4b7a45d729de617ff3374bc2e7ad1fbd.jpg
120	Mazzi Wheels	med	https://kxwheels.s3.amazonaws.com/cache/31/8c/318c15785937bdcc08141946e41c1158.jpg
122	Mayhem Wheels	med	https://kxwheels.s3.amazonaws.com/cache/0b/55/0b558cddb3b710804042783c274091ce.jpg
133	Concept One Wheels	med	https://kxwheels.s3.amazonaws.com/cache/fd/f2/fdf2abad21d917d52f8194d9b9f42b1b.jpg
136	Dip Wheels	med	https://kxwheels.s3.amazonaws.com/cache/de/2a/de2aceb9cb32d6f350156704dda75c4f.jpg
137	Dropstar Wheels	med	https://kxwheels.s3.amazonaws.com/cache/50/bb/50bbd4c9462c5e03639519a6fa3d6dc4.jpg
138	DUB Wheels	med	https://kxwheels.s3.amazonaws.com/cache/36/36/363693347fdb736918776097ca7ad2dc.jpg
56	Lorenzo Wheels	med	https://kxwheels.s3.amazonaws.com/cache/48/c0/48c0f0ef1c3f579b7127bb7cd5c4060d.jpg
65	Gianna Wheels	med	https://kxwheels.s3.amazonaws.com/cache/6c/4a/6c4ab56f8fa069c8f427525b59b11cf1.jpg
76	HD Wheels-HD Rims-HD	med	https://kxwheels.s3.amazonaws.com/cache/82/34/823490e934c02ff5c67f6589af19c00a.jpg
140	MSR Wheels	med	https://kxwheels.s3.amazonaws.com/cache/d5/cf/d5cfd86f938302dcd851dcba6be409a6.jpg
113	Moto Metal Offroad Wheels	med	https://kxwheels.s3.amazonaws.com/cache/73/eb/73eb4b9d47fc9644bbe7bc44191cbb95.jpg
145	Motiv Wheels	med	https://kxwheels.s3.amazonaws.com/cache/55/24/55243c2c919d68291affe4d450f7552c.jpg
87	Voxx Wheels	med	https://kxwheels.s3.amazonaws.com/cache/96/75/96753be3065cc82595996681f4670ab9.jpg
116	Trailer Wheels	med	https://kxwheels.s3.amazonaws.com/cache/ea/3c/ea3c726b29589dec432b2e59583f1cd7.jpg
147	Pacer Wheels	med	https://kxwheels.s3.amazonaws.com/cache/14/a0/14a0d9d45949a6334ca2b69aefcfedcc.jpg
118	Sacchi Wheels	med	https://kxwheels.s3.amazonaws.com/cache/2b/13/2b1383bf6549aaa717299f9ecd91c06d.jpg
73	TUFF Wheels	med	https://kxwheels.s3.amazonaws.com/cache/85/d3/85d3e39c40abe11666abdee702cd514e.jpg
148	Platinum Wheels	med	https://kxwheels.s3.amazonaws.com/cache/1b/f9/1bf9ec132698b06a117899de09d5e568.jpg
119	Touren Wheels	med	https://kxwheels.s3.amazonaws.com/cache/88/f7/88f7abf90e769fd5576dcba8d83b0b99.jpg
66	14 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/f4/6a/f46a879d4815bcc5146db78c113a1c38.jpg
149	SOTA Offroad Wheels 	med	https://kxwheels.s3.amazonaws.com/cache/42/d0/42d009bb7a700febe7d7476da535437c.jpg
150	SSC Wheels	med	https://kxwheels.s3.amazonaws.com/cache/f9/c3/f9c3f8f33cfae8223c37fae3bf95a9a4.jpg
94	RMR Wheels	med	https://kxwheels.s3.amazonaws.com/cache/76/21/76212ea93a703c5c11b473addd858078.jpg
54	V-TEC Truck Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a9/f7/a9f7725e37b8d5a917bfce379e202539.jpg
121	Ridler Wheels	med	https://kxwheels.s3.amazonaws.com/cache/02/d1/02d1d217d7e7f0389000ac03a8e7da14.jpg
69	Zenetti Wheels	med	https://kxwheels.s3.amazonaws.com/cache/54/44/5444ef949c099253f19b3553a97f2fe4.jpg
153	Walker Evans Racing Wheels	med	https://kxwheels.s3.amazonaws.com/cache/99/50/9950e009950f7798392110f5a7602663.jpg
104	POISON SPYDER	med	https://kxwheels.s3.amazonaws.com/cache/30/df/30df1629df09ab47d9ed863b064e11ae.jpg
74	XO Luxury Wheels	med	https://kxwheels.s3.amazonaws.com/cache/d0/57/d0577c839ca87ee5ee1b96e85f98d336.jpg
151	TIS Wheels	med	https://kxwheels.s3.amazonaws.com/cache/02/5b/025bbb9a2324db4df5a09de9fd91db28.jpg
61	17 Inch Wheel Specials	med	https://kxwheels.s3.amazonaws.com/cache/c3/fd/c3fd9eb0fe3e3c71097aa944abd1f530.jpg
126	Allied Aluminum Trailer Wheels	med	https://kxwheels.s3.amazonaws.com/cache/8d/08/8d08d87d2199376f614b7ee005c4b06d.jpg
80	Black Rock Offroad Wheels	med	https://kxwheels.s3.amazonaws.com/cache/6f/b7/6fb797e7a9330e728865b7f9695d85b1.jpg
52	Vertini Wheels	med	https://kxwheels.s3.amazonaws.com/cache/94/21/942178e1183bca18dce1caa241abca09.jpg
71	RUFF Racing Wheels	med	https://kxwheels.s3.amazonaws.com/cache/93/0a/930a7b07028b1e5ef7290df2918da792.jpg
78	Pinnacle Wheels	med	https://kxwheels.s3.amazonaws.com/cache/a5/39/a539dce57264c1540c77ab2c3ddc8586.jpg
106	Shelby Wheels	med	https://kxwheels.s3.amazonaws.com/cache/c1/f9/c1f92a2431dccaf0763f2dc59b17d871.jpg
112	Motegi Tuner Wheels	med	https://kxwheels.s3.amazonaws.com/cache/bb/73/bb738dcc72c5fb8bf9af8758555c6c90.jpg
114	XD SERIES BY KMC WHEELS	med	https://kxwheels.s3.amazonaws.com/cache/e9/0e/e90e090f5976b6972bb52c4690c08ce5.jpg
154	Worx Wheels	med	https://kxwheels.s3.amazonaws.com/cache/eb/c2/ebc2a36b02e6a2b4da7ee893d4e1b564.jpg
158	Privat Wheels	med	https://kxwheels.s3.amazonaws.com/cache/ed/8d/ed8d197e829fd6596f8d4aee06cd2659.jpg
47	V360 Forged Wheels	med	https://kxwheels.s3.amazonaws.com/cache/6e/96/6e96fe16c3950fe616b8ae409047d9d6.jpg
144	Monster Off-Road Wheels	med	https://kxwheels.s3.amazonaws.com/cache/5d/cb/5dcb3ef6659c92ec6e7f2cd3e4b44ed9.jpg
\.


--
-- Name: kx_wheelbrandimagesthumbnail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kxwheels
--

SELECT pg_catalog.setval('kx_wheelbrandimagesthumbnail_id_seq', 1, false);


--
-- Name: kx_wheelbrandimagesthumbnail_pkey; Type: CONSTRAINT; Schema: public; Owner: kxwheels; Tablespace: 
--

ALTER TABLE ONLY kx_wheelbrandimagesthumbnail
    ADD CONSTRAINT kx_wheelbrandimagesthumbnail_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

