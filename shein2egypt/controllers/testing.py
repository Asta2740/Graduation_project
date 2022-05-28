sizezList = [product.size1, product.size2, product.size3, product.size4, product.size5,
                                         product.size6, ]
                            for qqq in sizezList:
                                if 'Nothing' in sizezList:
                                    sizezList.remove('Nothing')

                            sizezList_odoo = sizezList
                            sizezList_odoo.extend(('1', '2', '3', '4', '5', '6'))
                            print(sizezList_odoo)
                            print(sizezList)

                            try:
                                for x in sizezList:

                                    val = request.env['product.attribute.value'].sudo().search([('name', '=', x,)])

                                    if sizezList_odoo[0] == x:
                                        size_1 = val
                                        if size_1:
                                            WhichSize = "F1"

                                    if sizezList_odoo[1] == x:
                                        size_2 = val
                                        if size_2:
                                            WhichSize = "F2"

                                    if sizezList_odoo[2] == x:
                                        size_3 = val
                                        if size_3:
                                            WhichSize = "F3"

                                    if sizezList_odoo[3] == x:
                                        size_4 = val
                                        if size_4:
                                            WhichSize = "F4"

                                    if sizezList_odoo[4] == x:
                                        size_5 = val
                                        if size_5:
                                            WhichSize = "F5"

                                    if sizezList_odoo[5] == x:
                                        size_6 = val
                                        if size_6:
                                            WhichSize = "F6"


                            except:
                                No_attribute = 0

                            try:
                                if size_1 and "F1" in WhichSize:
                                    ptal = request.env['product.template.attribute.line'].sudo().create({
                                        'attribute_id': Attribute.id if Attribute else False,
                                        'product_tmpl_id': x.id,
                                        'value_ids': [(6, 0, [size_1.id])],
                                    })
                                    x.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})

                            except:
                                pass
                            try:
                                if size_2 and "F2" in WhichSize:
                                    ptal = request.env['product.template.attribute.line'].sudo().create({
                                        'attribute_id': Attribute.id if Attribute else False,
                                        'product_tmpl_id': x.id,
                                        'value_ids': [(6, 0, [size_1.id, size_2.id])],
                                    })
                                    x.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})
                            except:
                                pass
                            try:
                                if size_3 and "F3" in WhichSize:
                                    ptal = request.env['product.template.attribute.line'].sudo().create({
                                        'attribute_id': Attribute.id if Attribute else False,
                                        'product_tmpl_id': x.id,
                                        'value_ids': [(6, 0, [size_1.id, size_2.id, size_3.id])],
                                    })
                                    x.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})
                            except:
                                pass
                            try:
                                if size_4 and "F4" in WhichSize:
                                    ptal = request.env['product.template.attribute.line'].sudo().create({
                                        'attribute_id': Attribute.id if Attribute else False,
                                        'product_tmpl_id': x.id,
                                        'value_ids': [(6, 0, [size_1.id, size_2.id, size_3.id, size_4.id])],
                                    })
                                    x.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})

                            except:
                                pass
                            try:
                                if size_5 and "F5" in WhichSize:
                                    ptal = request.env['product.template.attribute.line'].sudo().create({
                                        'attribute_id': Attribute.id if Attribute else False,
                                        'product_tmpl_id': x.id,
                                        'value_ids': [
                                            (6, 0, [size_1.id, size_2.id, size_3.id, size_4.id, size_5.id])],
                                    })
                                    x.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})
                            except:
                                pass
                            try:

                                if size_6 and "F6" in WhichSize:
                                    ptal = request.env['product.template.attribute.line'].sudo().create({
                                        'attribute_id': Attribute.id if Attribute else False,
                                        'product_tmpl_id': x.id,
                                        'value_ids': [
                                            (6, 0,
                                             [size_1.id, size_2.id, size_3.id, size_4.id, size_5.id, size_6.id])],
                                    })
                                    x.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})
                            except:
                                pass