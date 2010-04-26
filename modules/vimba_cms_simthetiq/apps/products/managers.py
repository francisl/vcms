# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.db import models
from django.contrib.sites.managers import CurrentSiteManager
from vcms.apps.www.fields import StatusField


class ProductPageManager(models.Manager):
    def reorder_product_position(self):
        """ reorder the complete product list
            run quite slowly because it need to query and save all product
            Only use to reorder when the list get corrupted
        """
        all_product = self.all()
        first = all_product[0]
        last = all_product[len(all_product)-1]
        first.previous = last
        first.save(reorder=False)
        last.next = first
        last.save(reorder=False)
        previous = None
        
        for product in all_product:
            if product == first:
                product.next = last
                last.previous = product
                product.save(reorder=False)
                last.save(reorder=False)
                previous = product
            elif product == last:
                if product.previous != previous:
                    product.previous = previous
                    product.save(reorder=False)
            else:
                if product.previous != previous:
                    product.previous = previous
                    product.save(reorder=False)
                if product.next != last:
                    product.next = last
                    product.save(reorder=False)
                if previous.next != product:
                    previous.next = product
                    previous.save(reorder=False)
                # make previous product equal to current for the next iteration
                previous = product
                
    def set_product_position(self, selected_product):
        """ Description : When a product is saved, this goes down the list
            It keep track of the previous product
            then it correct the previous, current and next product to link each other
        """
        
        all_product = self.all()    # all products
        # set to last product - simplify code if there's only one product or two
        previous_product = all_product[len(all_product)-1]
        next_product = all_product[len(all_product)-1]
        
        #selected_product.previous = previous_product
        #selected_product.next = next_product
        
        get_next_product = False
        for product in all_product:
            if product.slug == selected_product.slug:
                # found the product
                get_next_product = True
                previous_product.next = product
                selected_product.previous = previous_product
                previous_product.save(reorder=False)
                
            elif get_next_product:
                # only get in when the selected product is found and there's other product afterward 
                #print("get next product %s" % product)
                next_product = product
                next_product.previous = selected_product
                selected_product.next = next_product
                break
            else:
                # still not the selected product, keep new previous and go on
                previous_product = product
  
        if selected_product.slug == next_product.slug:
            # selected are the last one, so next should link to the first
            next_product = all_product[0]
            selected_product.next = next_product
            next_product.previous = selected_product

        next_product.save(reorder=False)
        selected_product.save(reorder=False)


    def set_previous_next_product(self, selected_product, previous_product, next_product):
        """ This will set the previous.next object to the selected object next
            and the next.previous to the selected object previous
            It requires to make a query of the object, because the save() wont have an effect on it
            since it's belong to the original function and it wont be committed
        """
        try:
            previous_p = self.get(id=previous_product.id)
            previous_p.next = next_product
            previous_p.save(reorder=False)
        except:
            #print("error setting previous product -> next")
            pass
        
        try:
            next_p = self.get(id=next_product.id)
            next_p.previous = previous_product
            next_p.save(reorder=False)
        except:
            #print("error setting next product -> previous")
            pass
            
           
    def remove_product_position(self, selected_product):
        """ LEGACY CODE
        """
        try:
            previous = self.get(id=selected_product.previous.id)
        except:
            #print("previous exception")
            previous = None
            selected_product.save()
            
        try: 
            next = self.get(id=selected_product.next.id)
        except:
            #print("next exception")
            next = None
            selected_product.save()
        
        #print("previous = %s" % previous)
        #print("next = %s" % next)    
        if previous != next and (previous == selected_product or next == selected_product):
            #print('no valid pointer to self')
            if previous == selected_product:
                #print('no valid pointer to self - previous')
                previous = None
            if next == selected_product:
                #print('no valid pointer to self - next')
                next = None
            
        if previous == next and previous != None:
            """ in condition there is only one product """
            #print("previous same as next")
            previous_product = previous
            previous_product.next = next
            previous_product.previous = previous
            previous_product.save(reorder=False)
        else:
            #print("else")
            if not next == None:
                next_product = next
                #print("next_product = %s:%d" % (next_product, id(next_product)))
                next_product.previous = previous
                next_product.save(reorder=False)
            
            if previous != None: 
                previous_product = previous
                previous_product.next = next
                #print("previous_product = %s:%d" % (previous_product, id(previous_product)))
                previous_product.save(reorder=False)

        return selected_product

    def remove_previous_link(self, selected_product):
        products_previous_link_to_selected = self.filter(previous=selected_product)
        #print("removing previous link to selected product (%s) : %s" % (selected_product,products_previous_link_to_selected) )

        for product in products_previous_link_to_selected:
            #print("delinking previous %s" % product)
            product.previous=None
            product.save(reorder=False)
    
    def remove_next_link(self, selected_product):
        products_next_link_to_selected = self.filter(next=selected_product)
        #print("removing next link to selected product (%s) : %s" % (selected_product,products_next_link_to_selected) )

        for product in products_next_link_to_selected:
            #print("delinking next %s" % product)
            product.next=None
            product.save(reorder=False)

    def get_available_products(self):
        #from vcms.apps.www.modelsimport Page
        return self.filter(status=StatusField.PUBLISHED)
       

class CompactNavigationGroupManager(models.Manager): 
    def get_navigation(self):
        from vcms.apps.vwm.tree import helper
        """ return navigation tree as a list containin tree node dictionary """ 
        nav = []
        for navgroup in self.all():
            nav.append(helper.create_tree_node(navgroup.name, url=navgroup.get_absolute_url()))
        print("compact nav data = %s" % nav)
        print("all data = %s" % self.all())
        return nav

