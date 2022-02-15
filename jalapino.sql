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
    id integer NOT NULL,
    email character varying(100) NOT NULL
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

COPY public.customers (auth0_id, address, name, phone, id, email) FROM stdin;
auth0|61f84916bf1df9007137d347	99 Some St., Town, State	TEST	1-234-5678910	3	test@test.com
auth0|61f84916bf1df9007137d347	99 Some St., Town, State	TEST2	1-234-5678910	5	test2@test.com
auth0|61f84916bf1df9007137d347	99 Some St., Town, State	TEST3	1-234-5678910	6	test3@test.com
\.


--
-- Data for Name: ingredients; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.ingredients (name, id) FROM stdin;
rice	1
delicata	2
radicchio	3
parsnip	4
chickpea	5
beef	6
mustard seed	7
double cream	8
garam masala	9
italian seasoning	10
raspberry	11
jalapeno	12
socca	13
avocado	14
blackberry	15
leek	16
rhubarb	17
kiwi fruit	18
amchoor	19
rum	20
butterbean	21
limpa	22
celery	23
water chestnut	24
milk	25
oregano	26
mint	27
spring onions	28
sea trout	29
persimmon	30
quince	31
butter	32
miso	33
celeriac	34
caramel	35
nectarine	36
breadfruit	37
date	38
aubergine	39
melon	40
black pepper	41
pesto	42
lettuce	43
plantain	44
garlic	45
tomato	46
red chili	47
pumpkin seed	48
blueberry	49
chocolate	50
onion	51
cinnamon	52
cream cheese	53
tofu	54
salmon	55
buttermilk	56
ginger	57
cabbage	58
cress	59
ham	60
eel	61
coriander	62
yeast	63
venison	64
broccoli	65
sesame	66
vanilla	67
parsley	68
white cabbage	69
pumpkin	70
creme fraiche	71
swede	72
pepper	73
prawn	74
gochu jang	75
honey	76
swordfish	77
prune	78
feta	79
blackcurrant	80
mushroom	81
egg	82
courgette	83
veal	84
onions	85
parmesan	86
olive oil	87
bacon	88
saffron	89
artichoke	90
cheshire cheese	91
crab	92
nutmeg	93
almond	94
pasta	95
tzatziki	96
snake	97
anise	98
curry leaf	99
arugula	100
mascarpone	101
orange	102
chicken	103
sweetcorn	104
wheat bran	105
carob	106
mango	107
potato	108
gherkin	109
lemon	110
chestnut	111
apple	112
bean	113
oil	114
longan	115
potatoes	116
brill	117
strawberry	118
peppercorn	119
yoghurt	120
pigeon	121
cheese	122
cucumber	123
squash	124
pear	125
ale	126
tempeh	127
flour	128
cumin	129
turmeric	130
weetabix	131
pork	132
beetroot	133
rice vinegar	134
chili	135
lamb	136
lime	137
cream	138
spinach	139
coconut	140
cardamom	141
mutton	142
peppermint	143
ricotta	144
herring	145
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
1	71
1	141
1	73
2	71
2	18
2	81
2	138
3	128
3	85
3	9
3	92
4	128
4	85
4	39
4	103
5	45
5	54
5	104
6	45
6	139
6	70
7	51
7	5
7	74
7	138
8	1
8	134
8	73
8	55
9	128
9	32
9	85
9	119
9	124
10	51
10	41
10	116
10	21
10	126
11	128
11	63
11	32
11	22
12	51
12	73
12	45
12	57
12	130
12	129
12	62
12	47
12	46
12	136
12	142
13	43
13	46
13	69
13	40
13	106
14	87
14	51
14	45
14	28
14	1
14	129
14	86
14	133
14	61
14	138
15	128
15	32
15	85
15	126
15	136
16	51
16	79
16	88
17	51
17	41
17	116
17	111
17	64
18	128
18	32
18	85
18	48
18	31
19	43
19	77
19	119
20	51
20	3
20	62
21	128
21	63
21	114
21	85
21	132
21	6
22	128
22	63
22	114
22	85
22	27
22	66
23	43
23	66
23	100
24	43
24	96
24	145
25	51
25	73
25	45
25	57
25	130
25	129
25	62
25	47
25	46
25	81
25	19
26	128
26	63
26	114
26	122
26	82
26	144
27	46
27	51
27	45
27	95
27	26
27	41
27	82
27	14
28	51
28	73
28	45
28	57
28	130
28	129
28	62
28	47
28	46
28	7
28	98
29	128
29	32
29	85
29	50
29	76
30	128
30	32
30	82
30	141
30	83
31	128
31	32
31	125
31	38
32	128
32	32
32	85
32	67
32	78
33	128
33	32
33	82
33	25
33	104
33	56
34	128
34	32
34	82
34	38
34	70
35	128
35	32
35	82
35	38
35	48
36	128
36	32
36	67
36	8
36	101
36	80
36	11
37	128
37	32
37	82
37	135
37	110
38	128
38	32
38	67
38	8
38	53
38	35
38	20
39	45
39	111
40	51
40	33
40	72
41	128
41	85
41	124
41	36
42	128
42	85
42	34
42	139
43	128
43	85
43	58
43	62
44	51
44	24
44	2
45	43
45	105
45	10
46	69
46	123
46	43
46	29
46	127
47	43
47	143
47	119
48	43
48	117
48	66
49	128
49	32
49	137
49	49
50	51
50	116
50	103
50	73
51	73
51	90
51	34
52	43
52	46
52	69
52	92
52	38
53	51
53	23
53	4
54	51
54	73
54	45
54	57
54	130
54	62
54	52
54	70
54	140
55	128
55	63
55	114
55	82
55	135
56	43
56	69
56	123
56	115
56	75
57	87
57	51
57	45
57	28
57	1
57	86
57	89
57	138
58	128
58	104
58	92
59	46
59	43
59	69
59	91
59	37
60	123
60	59
60	43
60	109
60	15
61	43
61	123
61	59
61	97
61	130
62	51
62	73
62	45
62	57
62	130
62	62
62	99
62	70
62	44
63	128
63	85
63	12
63	141
64	45
64	16
64	120
64	138
65	1
65	134
65	82
65	81
66	128
66	85
66	119
66	103
67	123
67	43
67	59
67	106
67	45
68	71
68	135
68	18
69	1
69	134
69	55
69	39
70	128
70	42
70	84
71	128
71	85
71	30
71	36
72	128
72	85
72	144
72	39
73	128
73	121
73	103
74	128
74	32
74	82
74	25
74	103
74	50
75	128
75	32
75	82
75	118
75	38
76	128
76	32
76	82
76	25
76	13
76	65
77	128
77	32
77	85
77	66
77	48
78	128
78	32
78	82
78	25
78	101
78	112
79	128
79	32
79	67
79	8
79	53
79	17
79	40
80	128
80	32
80	82
80	61
80	113
81	128
81	32
81	82
81	94
81	76
82	128
82	32
82	82
82	25
82	60
82	107
83	128
83	32
83	85
83	78
83	50
84	128
84	85
84	119
84	39
85	128
85	63
85	32
85	131
85	56
86	128
86	63
86	114
86	112
86	14
87	128
87	32
87	82
87	25
87	80
87	122
88	128
88	32
88	82
88	108
88	93
89	128
89	63
89	32
89	85
89	68
89	16
90	128
90	63
90	32
90	85
90	108
91	128
91	63
91	32
91	85
91	57
91	73
92	128
92	85
92	141
92	30
93	128
93	32
93	82
93	38
93	102
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: nullfame
--

COPY public.orders (restaurant_id, customer_id, id) FROM stdin;
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
auth0|61f848d190b60f0070f2f294	The Confused Chef	https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/food-ga4666f1ca_640.jpg	He used to have a hat, now he's a confused chef!	Schloßstraße 16, 01067 Dresden, Germany	info@confused-chef.com	+1 582-202-3209	www.confused-chef.com	2
auth0|61f848d190b60f0070f2f294	U10 Seals	https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/shish-kebab-g4afb5ccab_640.jpg	Formerly known as Kee Chen Where	84 Palisade Ave, 06611 Trumbull, Connecticut	orders@u10seals.com	+1 203-275-0665	www.u10seals.com	3
auth0|61f848d190b60f0070f2f294	Not Necessarily BBQ	https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/food-g9be06d40f_640.jpg	It's not all sunshine and BBQ!	8601 Lindbergh Blvd, 19153 Philadelphia, Pennsylvania	hello@nn-bbq.com	+1 202-918-2132	www.nn-bbq.com	1
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.categories_id_seq', 12, true);


--
-- Name: customers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nullfame
--

SELECT pg_catalog.setval('public.customers_id_seq', 6, true);


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
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: nullfame
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


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

