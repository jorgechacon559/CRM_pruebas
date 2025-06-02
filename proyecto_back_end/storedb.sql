-- Crea la base de datos y usa el esquema
CREATE DATABASE IF NOT EXISTS storedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE storedb;

DROP TABLE IF EXISTS `detalle_venta`;
DROP TABLE IF EXISTS `ventas`;
DROP TABLE IF EXISTS `productos`;
DROP TABLE IF EXISTS `usuarios`;
DROP TABLE IF EXISTS `alembic_version`;

CREATE TABLE `usuarios` (
  `usuario_id` int NOT NULL AUTO_INCREMENT,
  `rol` varchar(50) NOT NULL DEFAULT 'usuario',
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `baja` tinyint(1) NOT NULL,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `productos` (
  `producto_id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` float NOT NULL,
  `stock` int NOT NULL,
  `baja` tinyint(1) NOT NULL,
  PRIMARY KEY (`producto_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `ventas` (
  `venta_id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fecha` date NOT NULL,
  `total` float NOT NULL,
  `cantidad_art` int NOT NULL,
  PRIMARY KEY (`venta_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `detalle_venta` (
  `detalle_venta_id` int NOT NULL AUTO_INCREMENT,
  `venta_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio` float NOT NULL,
  `total` float NOT NULL,
  PRIMARY KEY (`detalle_venta_id`),
  KEY `producto_id` (`producto_id`),
  KEY `venta_id` (`venta_id`),
  CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`producto_id`),
  CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`venta_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;