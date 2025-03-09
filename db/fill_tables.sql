INSERT INTO pymes_trust (ruc, pyme_name, trust_score, tier, next_tier) VALUES
                                             ('0381188260001', 'MOTO ESTADIO S.A.S.', 90, 'Platino', 0),
                                             ('0615573275001', 'COMERCIALIZADORA Y MANUFACTURAS NELMARAL S.A.S.', 85, 'Oro', 88),
                                             ('0651697942001', 'RUSTICOS, ACABADOS Y MARMOLES DE LA COSTA S.A.S.', 87, 'Oro', 33),
                                             ('1079358613001', 'LAS GALLINAS DORADAS SAS. EN LIQUIDACION JUDICIAL SIMPLIFICA',85, 'Oro', 15),
                                             ('0640519441001', 'CONSTRUCCIONES Y SUMINISTROS  JAL SAS', 92, 'Platino', 0),
                                             ('0106824134001', 'GRUPO EMPRESARIAL LUPA S.A.S.',85, 'Oro', 15),
                                             ('0117703309001', 'TRIMED DISTRIBUIDORA LTDA', 88, 'Oro', 12),
                                             ('1888304503001', 'E.P. SOLUCIONES SAS',81, 'Oro', 65),
                                             ('0166268081001', 'IMPEMP S.A.S.',89, 'Oro', 82),
                                             ('0851339947001', 'CONCRETOS Y PREFABRICADOS DEL CARIBE S.A.S.', 95, 'Platino', 0),
                                             ('2303308651001', 'GROUP ENGITECH S.A.S.', 73, 'Plata', 39),
                                             ('1628664537001', 'INVERCOM GROUP S.A.S. EN LIQUIDACION', 72, 'Plata', 39),
                                             ('0445687131001', 'SIERRA CABALLERO S.A.S. EN LIQUIDACION JUDICIAL', 76, 'Plata', 39),
                                             ('0862789733001', 'CARMONA RODRIGUEZ Y CIA S.A.S.', 81, 'Oro', 12),
                                             ('1000223008', 'RENOVADORA LA HUELLA S.A.S.', 87, 'Oro', 0),
                                             ('1000336710', 'RED-MEDIHOS S.A.S.,Sucumbíos', 83, 'Oro', 44),
                                             ('1006137571', 'CONSTRUCCIONES DAMAR A.C S.A.S.', 78, 'Plata', 39),
                                             ('1019283518', 'SUSTENTARCH S.A.S.', 78, 'Plata', 60),
                                             ('1033690567', 'CARTAGENA PLASTIC & RECONSTRUCTIVE SURGERY INSTITUTE SAS', 75, 'Plata', 0),
                                             ('1045568214', 'CONSTRUCTORA AAF S.A.S', 95, 'Platino', 0 ),
                                             ('1055059784', 'Filomena Peralta', 95, 'Platino', 0 ),
                                             ('1181753730', 'MEDISAN SAS',77, 'Plata', 44),
                                             ('1420424791', 'MEDICAL CARE LABORATORIOS LIMITADA',83, 'Oro', 13),
                                             ('1733580873', 'SOLUCIONES DIAGNOSTICAS PRADO LTDA',97, 'Platino', 0  ),
                                             ('1743559713', 'CAKE FACTORY TRADITION SAS', 80, 'Oro', 0 );
;

INSERT INTO mock_log_in (ruc, password) VALUES
                                            ('0381188260001', 'pssw123.'),
                                            ('0615573275001', 'pssw123.'),
                                            ('0651697942001', 'pssw123.'),
                                            ('1079358613001', 'pssw123.'),
                                            ('0640519441001', 'pssw123.'),
                                            ('0106824134001', 'pssw123.'),
                                            ('0117703309001', 'pssw123.'),
                                            ('1888304503001', 'pssw123.'),
                                            ('0166268081001', 'pssw123.'),
                                            ('0851339947001', 'pssw123.'),
                                            ('2303308651001', 'pssw123.'),
                                            ('1628664537001', 'pssw123.'),
                                            ('0445687131001', 'pssw123.'),
                                            ('0862789733001', 'pssw123.');

INSERT INTO
    credit_options (title, description, amount, interest_rate, term, requirements, recommended, link)
VALUES 
('Multicrédito', 'El préstamo de consumo ideal para realizar un viaje, llevar a cabo un proyecto o celebrar un evento.', 'Hasta $500,000 MXN', '13% anual', '12-48 meses', 'Nivel Básico o superior', FALSE, '/creditos/multicredito/'),
('Casafácil', 'Los préstamos hipotecarios perfectos para hacer realidad tu sueño de tener tu casa propia.', 'Hasta $5,000,000 MXN', '9% anual', '5-20 años', 'Nivel Plata o superior', TRUE, '/creditos/casafacil/'),
('Educativo', 'Préstamos para posgrados o especializaciones que puedes empezar a pagar cuando te gradúes.', 'Hasta $300,000 MXN', '8% anual', 'Hasta 60 meses', 'Nivel Básico o superior', FALSE, '/creditos/credito-educativo/'),
('Autofácil', 'El préstamo automotriz correcto para financiar tu carro nuevo o vehículos pesados para tu trabajo.', 'Hasta $1,500,000 MXN', '10% anual', '12-60 meses', 'Nivel Plata o superior', FALSE, '/creditos/autofacil/'),
('Microcrédito', 'El crédito PYME ideal para cubrir las necesidades de tu negocio e impulsar su crecimiento.', 'Hasta $1,000,000 MXN', '12% anual', '12-36 meses', 'Nivel Plata o superior', TRUE, '/microfinanzas/');

INSERT INTO
    mock_pymes (ruc, person_type, business_type, pyme_name, province, city, division, section, est_date, total_assets, size)
VALUES ('1000223008','Jurídica','Por Acciones Simplificadas','RENOVADORA LA HUELLA S.A.S.','Santo Domingo de los Tsáchilas','Santo Domingo','Fabricación de productos de caucho y de plástico', 'Industrias Manufactureras','2016-03-29',439087,'Pequeña')
