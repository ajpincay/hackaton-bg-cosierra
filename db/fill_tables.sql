INSERT INTO pymes_trust (ruc, pyme_name) VALUES
                                             ('0381188260001', 'MOTO ESTADIO S.A.S.'),
                                             ('0615573275001', 'COMERCIALIZADORA Y MANUFACTURAS NELMARAL S.A.S.'),
                                             ('0651697942001', 'RUSTICOS, ACABADOS Y MARMOLES DE LA COSTA S.A.S.'),
                                             ('1079358613001', 'LAS GALLINAS DORADAS SAS. EN LIQUIDACION JUDICIAL SIMPLIFICA'),
                                             ('0640519441001', 'CONSTRUCCIONES Y SUMINISTROS  JAL SAS'),
                                             ('0106824134001', 'GRUPO EMPRESARIAL LUPA S.A.S.'),
                                             ('0117703309001', 'TRIMED DISTRIBUIDORA LTDA'),
                                             ('1888304503001', 'E.P. SOLUCIONES SAS'),
                                             ('0166268081001', 'IMPEMP S.A.S.'),
                                             ('0851339947001', 'CONCRETOS Y PREFABRICADOS DEL CARIBE S.A.S.'),
                                             ('2303308651001', 'GROUP ENGITECH S.A.S.'),
                                             ('1628664537001', 'INVERCOM GROUP S.A.S. EN LIQUIDACION'),
                                             ('0445687131001', 'SIERRA CABALLERO S.A.S. EN LIQUIDACION JUDICIAL'),
                                             ('0862789733001', 'CARMONA RODRIGUEZ Y CIA S.A.S.');

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


INSERT INTO pymes_trust (ruc, pyme_name) VALUES
                                             ('0381188260001', 'MOTO ESTADIO S.A.S.'),
                                             ('0615573275001', 'COMERCIALIZADORA Y MANUFACTURAS NELMARAL S.A.S.'),
                                             ('0651697942001', 'RUSTICOS, ACABADOS Y MARMOLES DE LA COSTA S.A.S.'),
                                             ('1079358613001', 'LAS GALLINAS DORADAS SAS. EN LIQUIDACION JUDICIAL SIMPLIFICA'),
                                             ('0640519441001', 'CONSTRUCCIONES Y SUMINISTROS  JAL SAS'),
                                             ('0106824134001', 'GRUPO EMPRESARIAL LUPA S.A.S.'),
                                             ('0117703309001', 'TRIMED DISTRIBUIDORA LTDA'),
                                             ('1888304503001', 'E.P. SOLUCIONES SAS'),
                                             ('0166268081001', 'IMPEMP S.A.S.'),
                                             ('0851339947001', 'CONCRETOS Y PREFABRICADOS DEL CARIBE S.A.S.'),
                                             ('2303308651001', 'GROUP ENGITECH S.A.S.'),
                                             ('1628664537001', 'INVERCOM GROUP S.A.S. EN LIQUIDACION'),
                                             ('0445687131001', 'SIERRA CABALLERO S.A.S. EN LIQUIDACION JUDICIAL'),
                                             ('0862789733001', 'CARMONA RODRIGUEZ Y CIA S.A.S.');


INSERT INTO credit_options (title, description, amount, interest_rate, term, requirements, recommended, link)
VALUES 
('Multicrédito', 'El préstamo de consumo ideal para realizar un viaje, llevar a cabo un proyecto o celebrar un evento.', 'Hasta $500,000 MXN', '13% anual', '12-48 meses', 'Nivel Básico o superior', FALSE, '/creditos/multicredito/'),
('Casafácil', 'Los préstamos hipotecarios perfectos para hacer realidad tu sueño de tener tu casa propia.', 'Hasta $5,000,000 MXN', '9% anual', '5-20 años', 'Nivel Plata o superior', TRUE, '/creditos/casafacil/'),
('Educativo', 'Préstamos para posgrados o especializaciones que puedes empezar a pagar cuando te gradúes.', 'Hasta $300,000 MXN', '8% anual', 'Hasta 60 meses', 'Nivel Básico o superior', FALSE, '/creditos/credito-educativo/'),
('Autofácil', 'El préstamo automotriz correcto para financiar tu carro nuevo o vehículos pesados para tu trabajo.', 'Hasta $1,500,000 MXN', '10% anual', '12-60 meses', 'Nivel Plata o superior', FALSE, '/creditos/autofacil/'),
('Microcrédito', 'El crédito PYME ideal para cubrir las necesidades de tu negocio e impulsar su crecimiento.', 'Hasta $1,000,000 MXN', '12% anual', '12-36 meses', 'Nivel Plata o superior', TRUE, '/microfinanzas/');
