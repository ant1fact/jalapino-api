--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO nullfame;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.categories (
    name character varying(50) NOT NULL,
    restaurant_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.categories OWNER TO nullfame;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: nullfame
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO nullfame;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nullfame
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.customers (
    auth0_id character varying(50) NOT NULL,
    address character varying(250) NOT NULL,
    name character varying(50) NOT NULL,
    phone character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.customers OWNER TO nullfame;

--
-- Name: customers_id_seq; Type: SEQUENCE; Schema: public; Owner: nullfame
--

CREATE SEQUENCE public.customers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customers_id_seq OWNER TO nullfame;

--
-- Name: customers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nullfame
--

ALTER SEQUENCE public.customers_id_seq OWNED BY public.customers.id;


--
-- Name: ingredients; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.ingredients (
    name character varying(20) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.ingredients OWNER TO nullfame;

--
-- Name: ingredients_id_seq; Type: SEQUENCE; Schema: public; Owner: nullfame
--

CREATE SEQUENCE public.ingredients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ingredients_id_seq OWNER TO nullfame;

--
-- Name: ingredients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nullfame
--

ALTER SEQUENCE public.ingredients_id_seq OWNED BY public.ingredients.id;


--
-- Name: items; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.items (
    description character varying(250),
    name character varying(50) NOT NULL,
    price numeric(5,2) NOT NULL,
    category_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.items OWNER TO nullfame;

--
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: nullfame
--

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.items_id_seq OWNER TO nullfame;

--
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nullfame
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- Name: items_ingredients; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.items_ingredients (
    item_id integer NOT NULL,
    ingredient_id integer NOT NULL
);


ALTER TABLE public.items_ingredients OWNER TO nullfame;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.orders (
    restaurant_id integer NOT NULL,
    customer_id integer NOT NULL,
    is_completed boolean NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.orders OWNER TO nullfame;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: nullfame
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO nullfame;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nullfame
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: orders_items; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.orders_items (
    orders_id integer NOT NULL,
    item_id integer NOT NULL
);


ALTER TABLE public.orders_items OWNER TO nullfame;

--
-- Name: restaurants; Type: TABLE; Schema: public; Owner: nullfame
--

CREATE TABLE public.restaurants (
    auth0_id character varying(50) NOT NULL,
    name character varying(50) NOT NULL,
    logo_uri character varying(250),
    description character varying(250),
    address character varying(250) NOT NULL,
    email character varying(100) NOT NULL,
    phone character varying(50) NOT NULL,
    website character varying(250),
    id integer NOT NULL
);


ALTER TABLE public.restaurants OWNER TO nullfame;

--
-- Name: restaurants_id_seq; Type: SEQUENCE; Schema: public; Owner: nullfame
--

CREATE SEQUENCE public.restaurants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.restaurants_id_seq OWNER TO nullfame;

--
-- Name: restaurants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nullfame
--

ALTER SEQUENCE public.restaurants_id_seq OWNED BY public.restaurants.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: customers id; Type: DEFAULT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.customers ALTER COLUMN id SET DEFAULT nextval('public.customers_id_seq'::regclass);


--
-- Name: ingredients id; Type: DEFAULT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.ingredients ALTER COLUMN id SET DEFAULT nextval('public.ingredients_id_seq'::regclass);


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: restaurants id; Type: DEFAULT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.restaurants ALTER COLUMN id SET DEFAULT nextval('public.restaurants_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.alembic_version (version_num) FROM stdin;
74f4769b8f09
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.categories (name, restaurant_id, id) FROM stdin;
Appetizers	1	1
Mains	1	2
Desserts	1	3
Drinks	1	4
Starters	2	5
Pizza	2	6
Burgers	2	7
Drinks	2	8
Dips	3	9
Puddings	3	10
Vegetarian	3	11
Drinks	3	12
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.customers (auth0_id, address, name, phone, id) FROM stdin;
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.ingredients (name, id) FROM stdin;
yoghurt	1
breadfruit	2
strawberry	3
onions	4
pear	5
red chili	6
squash	7
mint	8
date	9
olive oil	10
limpa	11
pasta	12
peppercorn	13
cress	14
rice vinegar	15
tomato	16
potato	17
nutmeg	18
cumin	19
radicchio	20
chocolate	21
turmeric	22
chicken	23
sea trout	24
rum	25
wheat bran	26
bean	27
curry leaf	28
ginger	29
buttermilk	30
tofu	31
water chestnut	32
herring	33
rice	34
persimmon	35
prawn	36
nectarine	37
veal	38
amchoor	39
brill	40
artichoke	41
creme fraiche	42
blackberry	43
pumpkin seed	44
ricotta	45
cardamom	46
quince	47
chili	48
delicata	49
mustard seed	50
cucumber	51
oil	52
prune	53
mutton	54
leek	55
saffron	56
venison	57
caramel	58
beef	59
broccoli	60
chestnut	61
sweetcorn	62
socca	63
black pepper	64
melon	65
parsley	66
gherkin	67
mushroom	68
celery	69
spinach	70
lamb	71
courgette	72
beetroot	73
coconut	74
arugula	75
garlic	76
cabbage	77
butterbean	78
ale	79
pesto	80
almond	81
apple	82
crab	83
peppermint	84
egg	85
parmesan	86
cinnamon	87
pigeon	88
avocado	89
garam masala	90
lettuce	91
cream cheese	92
snake	93
rhubarb	94
white cabbage	95
raspberry	96
italian seasoning	97
cream	98
oregano	99
swede	100
yeast	101
orange	102
pork	103
weetabix	104
flour	105
spring onions	106
blackcurrant	107
salmon	108
mango	109
double cream	110
eel	111
mascarpone	112
celeriac	113
pumpkin	114
feta	115
vanilla	116
cheese	117
longan	118
potatoes	119
carob	120
bacon	121
tempeh	122
cheshire cheese	123
pepper	124
lemon	125
blueberry	126
aubergine	127
anise	128
lime	129
gochu jang	130
swordfish	131
tzatziki	132
kiwi fruit	133
jalapeno	134
plantain	135
onion	136
parsnip	137
coriander	138
butter	139
honey	140
sesame	141
milk	142
ham	143
miso	144
chickpea	145
\.


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.items (description, name, price, category_id, id) FROM stdin;
A dip made from black cardamom and yellow pepper.	Cardamom and pepper dip	1.49	1	1
A dip made from fresh kiwi fruit and chanterelle mushroom.	Kiwi fruit and mushroom dip	1.49	1	2
Thin filo pastry cases stuffed with garam masala and crab.	Garam masala and crab parcels	2.99	1	3
Thin wonton cases stuffed with marinaded aubergine and corn-fed chicken.	Aubergine and chicken wontons	2.99	1	4
Tofu and baby sweetcorn combined into smooth soup.	Tofu and sweetcorn soup	3.49	1	5
Fresh spinach and spiced pumpkin combined into smooth soup.	Spinach and pumpkin soup	3.99	1	6
Fresh chickpea and king prawns combined into creamy soup.	Chickpea and prawn soup	4.99	1	7
Toasted seaweed wrapped around sushi rice, filled with sweet pepper and freshly-caught salmon.	Pepper and salmon maki	4.99	1	8
Pink peppercorn and acorn squash topped with butter crumble.	Peppercorn and squash crumble	9.72	2	9
Butterbean and ale stewed.	Butterbean and ale stew	9.36	2	10
Fluffy bread made with limpa and.	Limpa and bread	8.82	2	11
Medium-hot madras made with succulent lamb and mutton.	Lamb and mutton madras	16.38	2	12
A crunchy salad featuring honeydew melon and carob.	Melon and carob salad	7.92	2	13
Creamy risotto rice with fresh beetroot and eel.	Beetroot and eel risotto	15.12	2	14
A flaky pasty case filled with ale and minced lamb.	Ale and lamb pie	8.10	2	15
Tangy feta and smoked bacon combined into chunky soup.	Feta and bacon soup	3.24	2	16
Roasted chestnut and venison stewed.	Chestnut and venison casserole	9.72	2	17
Pumpkin seeds and fresh quince topped with butter crumble.	Pumpkin seed and quince crumble	10.08	2	18
Swordfish and black peppercorn served on a bed of lettuce.	Swordfish and peppercorn salad	5.40	2	19
Crunchy stir fry featuring fresh radicchio and coriander.	Radicchio and coriander stir fry	4.86	2	20
Succulent burgers made from pork and beef, served in a roll.	Pork and beef burgers	10.26	2	21
Sizzling sausages made from dried mint and sesame, served in a roll.	Mint and sesame sausages	10.62	2	22
Sesame and fresh arugula served on a bed of lettuce.	Sesame and arugula salad	4.32	2	23
Tzatziki and herring served on a bed of lettuce.	Tzatziki and herring salad	4.68	2	24
Medium-hot madras made with hand-picked mushroom and amchoor.	Mushroom and amchoor madras	17.28	2	25
Deep pan pizza topped with free range eggs and ricotta.	Egg and ricotta pizza	10.62	2	26
Fresh egg pasta in a sauce made from free range eggs and fresh avocado.	Egg and avocado fusilli	11.70	2	27
Medium-hot madras made with black mustard seeds and fresh anise.	Mustard seed and anise madras	17.64	2	28
A rich suet pudding made with plain chocolate and clover honey.	Chocolate and honey pudding	9.36	3	29
Crumbly buns made with black cardamom and yellow courgette.	Cardamom and courgette buns	8.28	3	30
A rich suet pudding made with juicy pears and crunchy date.	Pear and date pudding	8.10	3	31
A rich suet pudding made with vanilla and fresh prune.	Vanilla and prune pudding	9.00	3	32
Crispy crepes filled with baby sweetcorn and creamy buttermilk.	Sweetcorn and buttermilk crepes	8.46	3	33
Moist cake made with crunchy date and fresh pumpkin.	Date and pumpkin cake	7.20	3	34
Fluffy cupcakes made with moist date and pumpkin seeds.	Date and pumpkin seed cupcakes	8.10	3	35
A velvety cheesecake layered with fresh blackcurrant and raspberry.	Blackcurrant and raspberry cheesecake	15.66	3	36
Moist cake made with hot chili and fresh lemon.	Chili and lemon cake	7.20	3	37
A luxurious cheesecake layered with caramel and rum.	Caramel and rum cheesecake	14.04	3	38
Roasted chestnut and fresh garlic combined into chunky soup.	Chestnut and garlic soup	2.88	5	39
Brown miso and swede combined into chunky soup.	Miso and swede soup	3.24	5	40
Thin pastry cases stuffed with pattypan squash and fresh nectarine.	Squash and nectarine dumplings	8.10	5	41
Thin pastry cases stuffed with fresh celeriac and spinach.	Celeriac and spinach gyoza	8.10	5	42
Thin pastry cases stuffed with fresh cabbage and coriander.	Cabbage and coriander gyoza	8.28	5	43
Crunchy stir fry featuring fresh water chestnut and delicata.	Water chestnut and delicata stir fry	5.58	6	44
Wheat bran and italian seasoning served on a bed of lettuce.	Wheat bran and italian seasoning salad	6.84	6	45
A crisp salad featuring sea trout and tempeh.	Sea trout and tempeh salad	9.18	6	46
Peppermint and green peppercorn served on a bed of lettuce.	Peppermint and peppercorn salad	5.58	6	47
Brill and sesame served on a bed of lettuce.	Brill and sesame salad	3.96	6	48
A flaky pasty case filled with fresh lime and blueberry.	Lime and blueberry pie	5.40	6	49
Corn-fed chicken and baby pepper stewed.	Chicken and pepper stew	8.28	6	50
Crunchy stir fry featuring fresh artichoke and celeriac.	Artichoke and celeriac stir fry	5.04	6	51
A crunchy salad featuring crab and crunchy date.	Crab and date salad	7.56	6	52
Crunchy stir fry featuring fresh celery and baby parsnips.	Celery and parsnip stir fry	3.96	6	53
Hot vindaloo made with fresh pumpkin and coconut.	Pumpkin and coconut vindaloo	12.54	7	54
Hot slices of bread filled with free range eggs and scotch bonnet chilli.	Egg and chilli toastie	5.40	7	55
A crisp salad featuring fresh longan and gochu jang.	Longan and gochu jang salad	9.36	7	56
Creamy risotto rice with saffron and taleggio.	Saffron and taleggio risotto	11.84	7	57
Thin pastry cases stuffed with baby sweetcorn and crab.	Sweetcorn and crab gyoza	3.96	7	58
A crisp salad featuring cheshire cheese and breadfruit.	Cheshire cheese and breadfruit salad	10.62	7	59
A crisp salad featuring gherkin and fresh blackberry.	Gherkin and blackberry salad	8.10	7	60
A crunchy salad featuring snake and turmeric.	Snake and turmeric salad	7.20	7	61
Spicy curry made with spiced pumpkin and fresh plantain.	Pumpkin and plantain curry	11.36	7	62
Thin filo pastry cases stuffed with fresh jalapeno and green cardamom.	Jalapeno and cardamom parcels	5.94	7	63
Fresh leek and natural yoghurt combined into creamy soup.	Leek and yoghurt soup	5.04	9	64
Pasta in a sauce made from free range eggs and wild mushroom.	Egg and mushroom uramaki	5.94	9	65
Thin filo pastry cases stuffed with black peppercorn and free range chicken.	Peppercorn and chicken parcels	6.12	9	66
A mouth-watering carob salad served with garlic dressing.	Carob salad with garlic dressing	7.02	9	67
A dip made from scotch bonnet chilli and fresh kiwi fruit.	Chilli and kiwi fruit dip	5.94	9	68
Pasta in a sauce made from smoked salmon and fresh aubergine.	Salmon and aubergine uramaki	6.66	9	69
Thin pastry cases stuffed with sun-dried tomato pesto and veal.	Pesto and veal gyoza	3.24	9	70
Thin wonton cases stuffed with fresh persimmon and nectarine.	Persimmon and nectarine wontons	6.30	9	71
Thin pastry cases stuffed with ricotta and fried aubergine.	Ricotta and aubergine dumplings	5.94	9	72
Thin pastry cases stuffed with pigeon and free range chicken.	Pigeon and chicken gyoza	3.96	9	73
Crispy pancake filled with corn-fed chicken and milk chocolate.	Chicken and chocolate pancake	7.92	10	74
Moist buns made with fresh strawberries and moist date.	Strawberry and date buns	6.48	10	75
Fluffy pancake filled with socca and fresh broccoli.	Socca and broccoli pancake	7.38	10	76
Sesame and pumpkin seeds topped with crunchy crumble.	Sesame and pumpkin seed crumble	7.74	10	77
Fluffy crepes filled with mascarpone and green apple.	Mascarpone and apple crepes	7.74	10	78
A velvety cheesecake layered with fresh rhubarb and honeydew melon.	Rhubarb and melon cheesecake	11.88	10	79
Moist cake made with eel and bean.	Eel and bean cake	5.22	10	80
Fluffy muffins made with flaked almond and clear honey.	Almond and honey muffins	5.94	10	81
Crispy crepes filled with smoked ham and fresh mango.	Ham and mango crepes	6.48	10	82
A rich suet pudding made with fresh prune and white chocolate.	Prune and chocolate pudding	7.02	10	83
Thin pastry cases stuffed with pink peppercorn and chargrilled aubergine.	Peppercorn and aubergine gyoza	6.48	11	84
Crunchy bread made with weetabix and creamy buttermilk.	Weetabix and buttermilk bread	7.56	11	85
A warm bagel filled with dessert apple and fresh avocado.	Apple and avocado bagel	5.94	11	86
Fluffy pancake filled with fresh blackcurrant and smoked cheese.	Blackcurrant and cheese pancake	8.28	11	87
Moist cake made with baby new potato and nutmeg.	Potato and nutmeg cake	6.12	11	88
Fluffy bread made with fresh parsley and frizzled leek.	Parsley and leek bread	7.74	11	89
Fluffy bread made with spelt and fresh potato.	Spelt and potato loaf	5.74	11	90
Fluffy bread made with root ginger and sweet pepper.	Ginger and pepper loaf	7.92	11	91
Thin filo pastry cases stuffed with black cardamom and fresh persimmon.	Cardamom and persimmon parcels	6.12	11	92
Rich cake made with moist date and fresh orange.	Date and orange cake	5.76	11	93
\.


--
-- Data for Name: items_ingredients; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.items_ingredients (item_id, ingredient_id) FROM stdin;
1	42
1	46
1	124
2	42
2	133
2	68
2	98
3	105
3	4
3	90
3	83
4	105
4	4
4	127
4	23
5	76
5	31
5	62
6	76
6	70
6	114
7	136
7	145
7	36
7	98
8	34
8	15
8	124
8	108
9	105
9	139
9	4
9	13
9	7
10	136
10	64
10	119
10	78
10	79
11	105
11	101
11	139
11	11
12	136
12	124
12	76
12	29
12	22
12	19
12	138
12	6
12	16
12	71
12	54
13	91
13	16
13	95
13	65
13	120
14	10
14	136
14	76
14	106
14	34
14	19
14	86
14	73
14	111
14	98
15	105
15	139
15	4
15	79
15	71
16	136
16	115
16	121
17	136
17	64
17	119
17	61
17	57
18	105
18	139
18	4
18	44
18	47
19	91
19	131
19	13
20	136
20	20
20	138
21	105
21	101
21	52
21	4
21	103
21	59
22	105
22	101
22	52
22	4
22	8
22	141
23	91
23	141
23	75
24	91
24	132
24	33
25	136
25	124
25	76
25	29
25	22
25	19
25	138
25	6
25	16
25	68
25	39
26	105
26	101
26	52
26	117
26	85
26	45
27	16
27	136
27	76
27	12
27	99
27	64
27	85
27	89
28	136
28	124
28	76
28	29
28	22
28	19
28	138
28	6
28	16
28	50
28	128
29	105
29	139
29	4
29	21
29	140
30	105
30	139
30	85
30	46
30	72
31	105
31	139
31	5
31	9
32	105
32	139
32	4
32	116
32	53
33	105
33	139
33	85
33	142
33	62
33	30
34	105
34	139
34	85
34	9
34	114
35	105
35	139
35	85
35	9
35	44
36	105
36	139
36	116
36	110
36	112
36	107
36	96
37	105
37	139
37	85
37	48
37	125
38	105
38	139
38	116
38	110
38	92
38	58
38	25
39	76
39	61
40	136
40	144
40	100
41	105
41	4
41	7
41	37
42	105
42	4
42	113
42	70
43	105
43	4
43	77
43	138
44	136
44	32
44	49
45	91
45	26
45	97
46	95
46	51
46	91
46	24
46	122
47	91
47	84
47	13
48	91
48	40
48	141
49	105
49	139
49	129
49	126
50	136
50	119
50	23
50	124
51	124
51	41
51	113
52	91
52	16
52	95
52	83
52	9
53	136
53	69
53	137
54	136
54	124
54	76
54	29
54	22
54	138
54	87
54	114
54	74
55	105
55	101
55	52
55	85
55	48
56	91
56	95
56	51
56	118
56	130
57	10
57	136
57	76
57	106
57	34
57	86
57	56
57	98
58	105
58	62
58	83
59	16
59	91
59	95
59	123
59	2
60	51
60	14
60	91
60	67
60	43
61	91
61	51
61	14
61	93
61	22
62	136
62	124
62	76
62	29
62	22
62	138
62	28
62	114
62	135
63	105
63	4
63	134
63	46
64	76
64	55
64	1
64	98
65	34
65	15
65	85
65	68
66	105
66	4
66	13
66	23
67	51
67	91
67	14
67	120
67	76
68	42
68	48
68	133
69	34
69	15
69	108
69	127
70	105
70	80
70	38
71	105
71	4
71	35
71	37
72	105
72	4
72	45
72	127
73	105
73	88
73	23
74	105
74	139
74	85
74	142
74	23
74	21
75	105
75	139
75	85
75	3
75	9
76	105
76	139
76	85
76	142
76	63
76	60
77	105
77	139
77	4
77	141
77	44
78	105
78	139
78	85
78	142
78	112
78	82
79	105
79	139
79	116
79	110
79	92
79	94
79	65
80	105
80	139
80	85
80	111
80	27
81	105
81	139
81	85
81	81
81	140
82	105
82	139
82	85
82	142
82	143
82	109
83	105
83	139
83	4
83	53
83	21
84	105
84	4
84	13
84	127
85	105
85	101
85	139
85	104
85	30
86	105
86	101
86	52
86	82
86	89
87	105
87	139
87	85
87	142
87	107
87	117
88	105
88	139
88	85
88	17
88	18
89	105
89	101
89	139
89	4
89	66
89	55
90	105
90	101
90	139
90	4
90	17
91	105
91	101
91	139
91	4
91	29
91	124
92	105
92	4
92	46
92	35
93	105
93	139
93	85
93	9
93	102
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.orders (restaurant_id, customer_id, is_completed, id) FROM stdin;
\.


--
-- Data for Name: orders_items; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.orders_items (orders_id, item_id) FROM stdin;
\.


--
-- Data for Name: restaurants; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.restaurants (auth0_id, name, logo_uri, description, address, email, phone, website, id) FROM stdin;
auth0|61f848d190b60f0070f2f294	Not Necessarily BBQ	https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/bbq_256x256.png	It's not all sunshine and BBQ!	8601 Lindbergh Blvd, 19153 Philadelphia, Pennsylvania	hello@nn-bbq.com	+1 202-918-2132	www.nn-bbq.com	1
auth0|61f848d190b60f0070f2f294	The Confused Chef	https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/hat_256x256.png	He used to have a hat, now he's a confused chef!	Schloßstraße 16, 01067 Dresden, Germany	info@confused-chef.com	+1 582-202-3209	www.confused-chef.com	2
auth0|61f848d190b60f0070f2f294	U10 Seals	https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/utensils_256x256.png	Formerly known as Kee Chen Where	84 Palisade Ave, 06611 Trumbull, Connecticut	orders@u10seals.com	+1 203-275-0665	www.u10seals.com	3
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.categories_id_seq', 12, true);


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.customers_id_seq', 1, false);


--
-- Name: ingredients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.ingredients_id_seq', 145, true);


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.items_id_seq', 93, true);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: restaurants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.restaurants_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: customers customers_auth0_id_key; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_auth0_id_key UNIQUE (auth0_id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (id);


--
-- Name: ingredients ingredients_name_key; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_name_key UNIQUE (name);


--
-- Name: ingredients ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.ingredients
    ADD CONSTRAINT ingredients_pkey PRIMARY KEY (id);


--
-- Name: items_ingredients items_ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.items_ingredients
    ADD CONSTRAINT items_ingredients_pkey PRIMARY KEY (item_id, ingredient_id);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- Name: orders_items orders_items_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_pkey PRIMARY KEY (orders_id, item_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: restaurants restaurants_email_key; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_email_key UNIQUE (email);


--
-- Name: restaurants restaurants_name_key; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_name_key UNIQUE (name);


--
-- Name: restaurants restaurants_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.restaurants
    ADD CONSTRAINT restaurants_pkey PRIMARY KEY (id);


--
-- Name: categories categories_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(id);


--
-- Name: items items_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: items_ingredients items_ingredients_ingredient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.items_ingredients
    ADD CONSTRAINT items_ingredients_ingredient_id_fkey FOREIGN KEY (ingredient_id) REFERENCES public.ingredients(id);


--
-- Name: items_ingredients items_ingredients_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.items_ingredients
    ADD CONSTRAINT items_ingredients_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(id);


--
-- Name: orders_items orders_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: orders_items orders_items_orders_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders_items
    ADD CONSTRAINT orders_items_orders_id_fkey FOREIGN KEY (orders_id) REFERENCES public.orders(id);


--
-- Name: orders orders_restaurant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_restaurant_id_fkey FOREIGN KEY (restaurant_id) REFERENCES public.restaurants(id);


--
-- PostgreSQL database dump complete
--

