insert into usuarios (nombre, usuario, contrasena, rol) values
('Félix', 'felix', 'cambiar123', 'entrenador'),
('Capitán', 'capitan', 'cambiar123', 'capitan'),
('Coordinación Deportiva', 'coordinacion', 'cambiar123', 'coordinacion');

insert into competencias (nombre, tipo, fecha_inicio, fecha_fin) values
('Liga Municipal de Voleibol de Tulancingo', 'liga', '2026-08-30', '2026-12-13'),
('Torneo Regional de Universidades Tecnológicas y Politécnicas', 'torneo', '2026-12-04', '2026-12-06');

insert into jugadores (nombre, matricula, correo, telefono, edad, cuatrimestre, carrera, rama, posicion, numero_playera) values
('Ana Sofía Hernández', '1724110123', '1724110123@utectulancingo.edu.mx', '7750000001', 19, 4, 'TI e Innovación Digital', 'femenil', 'colocador', 7),
('Valeria Ramírez Cruz', '1724110457', '1724110457@utectulancingo.edu.mx', '7750000002', 20, 4, 'Mecatrónica', 'femenil', 'opuesto', 11),
('Luis Ángel Pérez Ruiz', '1724110311', '1724110311@utectulancingo.edu.mx', '7750000003', 20, 4, 'TI e Innovación Digital', 'varonil', 'colocador', 5),
('Diego Martínez Soto', '1725110488', '1725110488@utectulancingo.edu.mx', '7750000004', 19, 1, 'Contaduría', 'varonil', 'opuesto', 10);
