--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dump_sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dump_sites (
    id integer NOT NULL,
    name text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    tile_url text
);


ALTER TABLE public.dump_sites OWNER TO postgres;

--
-- Name: dump_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dump_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dump_sites_id_seq OWNER TO postgres;

--
-- Name: dump_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dump_sites_id_seq OWNED BY public.dump_sites.id;


--
-- Name: ndwi_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ndwi_data (
    id integer NOT NULL,
    tile_id integer NOT NULL,
    observation_date date NOT NULL,
    mean double precision,
    min double precision,
    max double precision,
    std_dev double precision,
    cloud_coverage double precision,
    source text DEFAULT 'Sentinel-2'::text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.ndwi_data OWNER TO postgres;

--
-- Name: ndwi_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ndwi_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ndwi_data_id_seq OWNER TO postgres;

--
-- Name: ndwi_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ndwi_data_id_seq OWNED BY public.ndwi_data.id;


--
-- Name: pollution_alerts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pollution_alerts (
    id integer NOT NULL,
    tile_id integer NOT NULL,
    alert_type text,
    severity text,
    detected_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    description text,
    triggered_by text DEFAULT 'System'::text,
    CONSTRAINT pollution_alerts_alert_type_check CHECK ((alert_type = ANY (ARRAY['NDWI'::text, 'SWIR'::text, 'Mixed'::text]))),
    CONSTRAINT pollution_alerts_severity_check CHECK ((severity = ANY (ARRAY['Low'::text, 'Medium'::text, 'High'::text])))
);


ALTER TABLE public.pollution_alerts OWNER TO postgres;

--
-- Name: pollution_alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pollution_alerts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pollution_alerts_id_seq OWNER TO postgres;

--
-- Name: pollution_alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pollution_alerts_id_seq OWNED BY public.pollution_alerts.id;


--
-- Name: swir_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.swir_data (
    id integer NOT NULL,
    tile_id integer NOT NULL,
    observation_date date NOT NULL,
    mean double precision,
    min double precision,
    max double precision,
    std_dev double precision,
    cloud_coverage double precision,
    source text DEFAULT 'Sentinel-2'::text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.swir_data OWNER TO postgres;

--
-- Name: swir_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.swir_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.swir_data_id_seq OWNER TO postgres;

--
-- Name: swir_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.swir_data_id_seq OWNED BY public.swir_data.id;


--
-- Name: tiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tiles (
    id integer NOT NULL,
    name text NOT NULL,
    coordinates public.geometry(Polygon,4326),
    bbox jsonb NOT NULL,
    true_color_url text,
    ndwi_url text,
    swir_url text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tiles OWNER TO postgres;

--
-- Name: tiles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tiles_id_seq OWNER TO postgres;

--
-- Name: tiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tiles_id_seq OWNED BY public.tiles.id;


--
-- Name: dump_sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dump_sites ALTER COLUMN id SET DEFAULT nextval('public.dump_sites_id_seq'::regclass);


--
-- Name: ndwi_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ndwi_data ALTER COLUMN id SET DEFAULT nextval('public.ndwi_data_id_seq'::regclass);


--
-- Name: pollution_alerts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pollution_alerts ALTER COLUMN id SET DEFAULT nextval('public.pollution_alerts_id_seq'::regclass);


--
-- Name: swir_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.swir_data ALTER COLUMN id SET DEFAULT nextval('public.swir_data_id_seq'::regclass);


--
-- Name: tiles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tiles ALTER COLUMN id SET DEFAULT nextval('public.tiles_id_seq'::regclass);


--
-- Data for Name: dump_sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dump_sites (id, name, latitude, longitude, description, created_at, updated_at, tile_url) FROM stdin;
4	Sala Al Jadida Dump 4	33.997062	-6.734155	Beside Café Belle Époque	2025-05-27 16:04:24.273163	2025-05-27 16:04:24.273163	https://tile.googleapis.com/v1/2dtiles/18/126168/104720?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
5	Sala Al Jadida Dump 5	33.996713	-6.72738	Lotissement Villa Roundabout	2025-05-27 16:04:24.273163	2025-05-27 16:04:24.273163	https://tile.googleapis.com/v1/2dtiles/18/126173/104721?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
6	Sala Al Jadida Dump 6	33.995454	-6.737531	Behind Pharmacie Mail Central	2025-05-27 16:04:24.273163	2025-05-27 16:04:24.273163	https://tile.googleapis.com/v1/2dtiles/18/126165/104722?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
7	Sala Al Jadida Dump 7	33.998994	-6.744242	Near Snack Aux Délices – Chez Driss	2025-05-27 16:04:24.273163	2025-05-27 16:04:24.273163	https://tile.googleapis.com/v1/2dtiles/18/126160/104719?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
1	Sala Al Jadida Dump 1	33.99071	-6.7416	Behind Atlas Avenue	2025-05-27 01:30:08.544559	2025-05-27 01:30:08.544559	https://tile.googleapis.com/v1/2dtiles/18/126162/104726?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
2	Sala Al Jadida Dump 2	33.988455	-6.738625	Near Av. Bouregreg	2025-05-27 16:04:24.273163	2025-05-27 16:04:24.273163	https://tile.googleapis.com/v1/2dtiles/18/126165/104728?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
3	Sala Al Jadida Dump 3	33.988703	-6.735363	Opposite Mosquée Ahssin	2025-05-27 16:04:24.273163	2025-05-27 16:04:24.273163	https://tile.googleapis.com/v1/2dtiles/18/126167/104728?session=AJVsH2x0LEorJ0m-uqrGHuX7HIxLFSK0NQtzOr7h6NOCdIc7lIaVrZQEtD7FA6hsE_gpF3bjLioGfiM0ixbVl2p3NQ&key=AIzaSyBLh7Ne17_AOYlYWTnqjLwphi6_czkVM30
\.


--
-- Data for Name: ndwi_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ndwi_data (id, tile_id, observation_date, mean, min, max, std_dev, cloud_coverage, source, created_at) FROM stdin;
\.


--
-- Data for Name: pollution_alerts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pollution_alerts (id, tile_id, alert_type, severity, detected_at, description, triggered_by) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: swir_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.swir_data (id, tile_id, observation_date, mean, min, max, std_dev, cloud_coverage, source, created_at) FROM stdin;
\.


--
-- Data for Name: tiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tiles (id, name, coordinates, bbox, true_color_url, ndwi_url, swir_url, created_at) FROM stdin;
1	tile_1	0103000020E6100000010000000500000060CD76F706591BC0DEDD91EBB204414060CD76F706591BC09A1386667B0341402008731F4E521BC09A1386667B0341402008731F4E521BC0DEDD91EBB204414060CD76F706591BC0DEDD91EBB2044140	{"maxLat": 34.036710211013755, "maxLon": -6.830376140018444, "minLat": 34.02720338389118, "minLon": -6.8369406381856095}	\N	\N	\N	2025-05-27 19:38:46.007523
2	tile_2	0103000020E61000000100000005000000400BFF3866521BC0C6BC750CC4034140400BFF3866521BC01859045858034140C0C72A1802411BC01859045858034140C0C72A1802411BC0C6BC750CC4034140400BFF3866521BC0C6BC750CC4034140	{"maxLat": 34.02942043064972, "maxLon": -6.8134845520125396, "minLat": 34.026133539317186, "minLon": -6.830468073431632}	\N	\N	\N	2025-05-27 19:38:46.007523
3	tile_3	0103000020E61000000100000005000000A0D1373711411BC09EC712C689034140A0D1373711411BC0143B2987B2024140C0F37029A1391BC0143B2987B2024140C0F37029A1391BC09EC712C689034140A0D1373711411BC09EC712C689034140	{"maxLat": 34.02764202038746, "maxLon": -6.806278846282055, "minLat": 34.021073241359915, "minLon": -6.813542235166466}	\N	\N	\N	2025-05-27 20:00:18.351916
4	tile_4	0103000020E610000001000000050000008043859DC33B1BC0AA86CECAB30241408043859DC33B1BC07027D84AC1014140C0421B8EEA381BC07027D84AC1014140C0421B8EEA381BC0AA86CECAB30241408043859DC33B1BC0AA86CECAB3024140	{"maxLat": 34.02111182293204, "maxLon": -6.80558225671183, "minLat": 34.013711314720126, "minLon": -6.808363400706071}	\N	\N	\N	2025-05-27 20:00:18.351916
5	tile_5	0103000020E6100000010000000500000060BA5531F13A1BC0CCA25C501C0241400076CC911F411BC0CCA25C501C0241400076CC911F411BC06694088DBB00414060BA5531F13A1BC06694088DBB00414060BA5531F13A1BC0CCA25C501C024140	{"maxLat": 34.01648907206763, "maxLon": -6.807560702187942, "minLat": 34.00572359961443, "minLon": -6.8135969906848}	\N	\N	\N	2025-05-27 20:00:18.351916
6	tile_6	0103000020E61000000100000005000000C0D38E8030401BC07EC64E5FC4004140C0D38E8030401BC0FCDB0D7E52FF4040205C25F55C361BC0FCDB0D7E52FF4040205C25F55C361BC07EC64E5FC4004140C0D38E8030401BC07EC64E5FC4004140	{"maxLat": 34.00599280687764, "maxLon": -6.80308898010756, "minLat": 33.99470496823048, "minLon": -6.812685021131017}	\N	\N	\N	2025-05-27 20:00:18.351916
7	tile_7	0103000020E61000000100000005000000C0BBBD873A381BC08698A83057FF4040C0BBBD873A381BC0CE36941B08FF4040009609EC562B1BC0CE36941B08FF4040009609EC562B1BC08698A83057FF4040C0BBBD873A381BC08698A83057FF4040	{"maxLat": 33.99484832985131, "maxLon": -6.7923237686968605, "minLat": 33.99243492829338, "minLon": -6.804910775142105}	\N	\N	\N	2025-05-27 20:00:18.351916
8	tile_8	0103000020E61000000100000005000000E07742EC0B2E1BC02685A3220CFF4040E07742EC0B2E1BC0BE32AD8E9EFE4040A085458DF6241BC0BE32AD8E9EFE4040A085458DF6241BC02685A3220CFF4040E07742EC0B2E1BC02685A3220CFF4040	{"maxLat": 33.99255784019833, "maxLon": -6.7860967706377835, "minLat": 33.98921378571457, "minLon": -6.794967357212926}	\N	\N	\N	2025-05-27 20:00:18.351916
9	tile_9	0103000020E610000001000000050000000042065226281BC0D47CD49A0DFF4040205032FDC2211BC0D47CD49A0DFF4040205032FDC2211BC0A42998ACCDFF40400042065226281BC0A42998ACCDFF40400042065226281BC0D47CD49A0DFF4040	{"maxLat": 33.99846417836969, "maxLon": -6.782970386691915, "minLat": 33.99260268569347, "minLon": -6.789208680755564}	\N	\N	\N	2025-05-27 20:00:18.351916
10	tile_10	0103000020E61000000100000005000000E08BFFC2F8211BC0A81923CC94FF4040206742A3BC191BC0A81923CC94FF4040206742A3BC191BC01E866CF702004140E08BFFC2F8211BC01E866CF702004140E08BFFC2F8211BC0A81923CC94FF4040	{"maxLat": 34.000090530386146, "maxLon": -6.775133658340366, "minLat": 33.99672843660238, "minLon": -6.783175513121904}	\N	\N	\N	2025-05-27 20:00:18.351916
11	tile_11	0103000020E610000001000000050000004017AACCD51B1BC05CEAEEEC9BFF40404017AACCD51B1BC060A74BAAE7FE4040A04B79B5D1151BC060A74BAAE7FE4040A04B79B5D1151BC05CEAEEEC9BFF40404017AACCD51B1BC05CEAEEEC9BFF4040	{"maxLat": 33.99694596925539, "maxLon": -6.771307788399014, "minLat": 33.99144486135515, "minLon": -6.7771827677550505}	\N	\N	\N	2025-05-27 20:00:18.351916
12	tile_12	0103000020E610000001000000050000004054219EF2151BC00EADBC4513FF40404054219EF2151BC076FFB76895FE404000CBC7695E101BC076FFB76895FE404000CBC7695E101BC00EADBC4513FF40404054219EF2151BC00EADBC4513FF4040	{"maxLat": 33.99277564728446, "maxLon": -6.7659851577943755, "minLat": 33.988934602587435, "minLon": -6.771433325561759}	\N	\N	\N	2025-05-27 20:00:18.351916
\.


--
-- Name: dump_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dump_sites_id_seq', 7, true);


--
-- Name: ndwi_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ndwi_data_id_seq', 1, false);


--
-- Name: pollution_alerts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pollution_alerts_id_seq', 1, false);


--
-- Name: swir_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.swir_data_id_seq', 1, false);


--
-- Name: tiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tiles_id_seq', 12, true);


--
-- Name: dump_sites dump_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dump_sites
    ADD CONSTRAINT dump_sites_pkey PRIMARY KEY (id);


--
-- Name: ndwi_data ndwi_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ndwi_data
    ADD CONSTRAINT ndwi_data_pkey PRIMARY KEY (id);


--
-- Name: pollution_alerts pollution_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pollution_alerts
    ADD CONSTRAINT pollution_alerts_pkey PRIMARY KEY (id);


--
-- Name: swir_data swir_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.swir_data
    ADD CONSTRAINT swir_data_pkey PRIMARY KEY (id);


--
-- Name: tiles tiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tiles
    ADD CONSTRAINT tiles_pkey PRIMARY KEY (id);


--
-- Name: ndwi_data ndwi_data_tile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ndwi_data
    ADD CONSTRAINT ndwi_data_tile_id_fkey FOREIGN KEY (tile_id) REFERENCES public.tiles(id) ON DELETE CASCADE;


--
-- Name: pollution_alerts pollution_alerts_tile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pollution_alerts
    ADD CONSTRAINT pollution_alerts_tile_id_fkey FOREIGN KEY (tile_id) REFERENCES public.tiles(id) ON DELETE CASCADE;


--
-- Name: swir_data swir_data_tile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.swir_data
    ADD CONSTRAINT swir_data_tile_id_fkey FOREIGN KEY (tile_id) REFERENCES public.tiles(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

