-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 12-12-2022 a las 16:08:05
-- Versión del servidor: 8.0.27
-- Versión de PHP: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `cac_bookflix`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

DROP TABLE IF EXISTS `libros`;
CREATE TABLE IF NOT EXISTS `libros` (
  `lid` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8_spanish_ci NOT NULL,
  `fecha_publicacion` varchar(25) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `categoria` set('Terror','Drama','Acción','Fantasía') CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL,
  `autor` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `imagen` varchar(255) COLLATE utf8_spanish_ci NOT NULL,
  `pdf` varchar(255) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`lid`, `titulo`, `descripcion`, `fecha_publicacion`, `categoria`, `autor`, `imagen`, `pdf`) VALUES
(1, 'Harry Potter y la Piedra Filosofal', 'Harry Potter se ha quedado huérfano y vive en casa de sus abominables tíos y del\r\ninsoportable primo Dudley. Harry se siente muy triste y solo, hasta que un buen\r\ndía recibe una carta que cambiará su vida para siempre', '26 de Junio de 1997', 'Fantasía', 'J. K. Rowling', 'https://i.imgur.com/hNCAlMJ.jpg', 'https://web.seducoahuila.gob.mx/biblioweb/upload/J.K.%20Rowling%20-%20La%20Piedra%20filosofal.pdf'),
(2, '1984', 'En una supuesta sociedad policial, el estado\r\nha conseguido el control total sobre el individuo.\r\nNo existe siquiera un resquicio para la intimidad personal: el sexo es un crimen, las emociones están prohibidas', '08 de Junio de 1949', 'Drama', 'George Orwell', 'https://i.imgur.com/sAjYXDI.jpeg', 'https://ocw.uca.es/pluginfile.php/1485/mod_resource/content/1/1984.pdf'),
(3, 'El Resplandor', 'Jack es un hombre abrumado por un pasado que va más allá de lo que él\r\npuede recordar y, no estamos hablando de sólo un problema de alcohol.\r\nLuego de aceptar un trabajo que supondrá un cambio en su vida, la sombra\r\nde su pasado', '25 de Diciembre de 1980', 'Terror', 'Stephen King', 'https://i.imgur.com/r0Ir8gq.jpeg', 'https://gualeguaychu.gov.ar/apps/dashboard/ftp/biblioteca/45/45.pdf'),
(4, 'Juego de Tronos: Canción de Hielo y Fuego', 'Tras el largo verano, el invierno se acerca a los Siete Reinos. Lord Eddard\r\nStark, señor de Invernalia, deja sus dominios para unirse a la corte del rey\r\nRobert Baratheon el Usurpador, hombre díscolo y otrora guerrero audaz\r\ncuyas mayores aficiones son c', '01 de Agosto de 1996', 'Acción', 'George Martin', 'https://i.imgur.com/OWJhgUy.jpeg', 'https://www.sev.gob.mx/clasesdesdecasa/documentos/17c08e45734090a3124426075040c7dcJuegodetronos1.pdf'),
(5, 'Harry Potter y la Cámara Secreta', 'Tras derrotar una vez más a lord Voldemort, su siniestro enemigo en Harry\r\nPotter y la piedra filosofal, Harry espera impaciente en casa de sus insoportables\r\ntíos el inicio del segundo curso del Colegio Hogwarts de Magia y hechicería', '02 de Julio de 1998', 'Fantasía', 'J. K. Rowling', 'https://i.imgur.com/yTUEXbq.jpeg', 'http://www.jfk.edu.ec/jfk/images/librospdf/J.K._Rowling_-_2Harry_Potter_y_la_Camara_secreta.pdf'),
(6, 'Alicia en el país de las Maravillas', 'La historia cuenta cómo una niña llamada Alicia cae por un agujero, encontrándose en un mundo peculiar y extraño, poblado por humanos y criaturas antropomórficas', '26 de Noviembre de 1865', 'Fantasía', 'Lewis Carroll', 'https://i.imgur.com/HiZu8DT.jpeg', 'https://www.ucm.es/data/cont/docs/119-2014-02-19-Carroll.AliciaEnElPaisDeLasMaravillas.pdf'),
(8, 'Drácula', 'El abogado Jonathan Harker descubre que, en el castillo del conde Drácula, este se comporta por las noches como un vampiro. Harker sigue a Drácula a Inglaterra, donde el conde busca nuevas víctimas, entre ellas, a Mina, la prometida de Harker', '26 de Mayo de 1897', 'Terror', 'Bram Stoker', 'https://i.imgur.com/c714RJR.jpeg', 'https://portalacademico.cch.unam.mx/materiales/al/cont/tall/tlriid/tlriid4/circuloLectores/docs/dracula.pdf');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
