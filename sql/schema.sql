-- USUARIOS
create table usuarios (
    id serial primary key,
    nombre varchar(100) not null,
    usuario varchar(50) not null unique,
    contrasena varchar(255) not null,
    rol varchar(20) not null check (rol in ('entrenador', 'capitan', 'coordinacion')),
    activo boolean not null default true
);

-- JUGADORES
create table jugadores (
    id serial primary key,
    nombre varchar(100) not null,
    matricula varchar(10) not null unique,
    correo varchar(100) not null,
    telefono varchar(10),
    edad integer not null check (edad between 15 and 60),
    cuatrimestre integer not null check (cuatrimestre between 1 and 11),
    carrera varchar(100) not null,
    rama varchar(10) not null check (rama in ('femenil', 'varonil')),
    posicion varchar(20) not null check (posicion in ('colocador', 'opuesto', 'central', 'receptor', 'libero')),
    numero_playera integer not null check (numero_playera between 0 and 99),
    estado varchar(10) not null default 'activo' check (estado in ('activo', 'baja')),
    fecha_ingreso date not null default current_date,
    unique (rama, numero_playera)
);

-- ENTRENAMIENTOS
create table entrenamientos (
    id serial primary key,
    fecha date not null,
    hora_inicio time not null,
    hora_fin time not null,
    rama varchar(10) not null check (rama in ('femenil', 'varonil')),
    tipo varchar(10) not null default 'fijo' check (tipo in ('fijo', 'extra')),
    estado varchar(15) not null default 'programado' check (estado in ('programado', 'cancelado')),
    check (hora_fin > hora_inicio),
    unique (fecha, hora_inicio, rama)
);

-- ASISTENCIAS
create table asistencias (
    id serial primary key,
    entrenamiento_id integer not null references entrenamientos(id),
    jugador_id integer not null references jugadores(id),
    estado varchar(15) not null check (estado in ('presente', 'falta', 'justificada')),
    motivo varchar(200),
    unique (entrenamiento_id, jugador_id),
    check (estado <> 'justificada' or length(motivo) >= 10)
);

-- COMPETENCIAS
create table competencias (
    id serial primary key,
    nombre varchar(150) not null,
    tipo varchar(10) not null check (tipo in ('liga', 'torneo')),
    fecha_inicio date not null,
    fecha_fin date not null,
    check (fecha_fin >= fecha_inicio)
);

-- PARTIDOS
create table partidos (
    id serial primary key,
    competencia_id integer references competencias(id),
    rama varchar(10) not null check (rama in ('femenil', 'varonil')),
    rival varchar(100) not null,
    fecha date not null,
    sets varchar(60),
    resultado varchar(10) check (resultado in ('ganado', 'perdido'))
);

-- DISPONIBILIDAD PARA LIGA
create table disponibilidad (
    id serial primary key,
    partido_id integer not null references partidos(id),
    jugador_id integer not null references jugadores(id),
    puede_asistir boolean not null,
    unique (partido_id, jugador_id)
);

-- CONVOCATORIAS A TORNEO
create table convocatorias (
    id serial primary key,
    competencia_id integer not null references competencias(id),
    jugador_id integer not null references jugadores(id),
    unique (competencia_id, jugador_id)
);
