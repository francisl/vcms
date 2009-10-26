# encoding: utf-8
# copyright Vimba inc. 2009
# programmer : Francis Lavoie

from django.db import models
from django.contrib.sites.managers import CurrentSiteManager

class ProductPageManager(models.Manager):
    def set_product_position(self, selected_product):

        all_product = self.all()
        previous_product = selected_product
        selected_product.next = selected_product
        selected_product.previous = selected_product
        
        #print("----------------------------------------")
        #print("Selected product = %s " % selected_product)
        for product in all_product:
            if product.slug == selected_product.slug:
                break
            else:
                previous_product = product
        
        """ Condition :
            there is only one product
                previous and next equal to selected_product
            the product is the first one
                previous equal last
                next equal last previous
            the product is the last one
                previous is the previous of last
                next is the fist one
            the product is somewhere in the middle
                previous is previous
                next is previous next
        """
        
        if len(all_product) <= 1:
            #print("Product is lonely")
            selected_product.next = selected_product
            selected_product.previous = selected_product
        elif previous_product == selected_product:
            #print("Product is the first one of many")
            previous_product = last_product = all_product[len(all_product)-1]
            if previous_product.next == previous_product:
                # there's only one product in the database
                # this correct a bug, when two object save the same object one after the other
                # the second save will be discard
                next_product = previous_product
            else:
                next_product = previous_product.next
                
            selected_product.previous = previous_product
            selected_product.next = next_product
            previous_product.next = selected_product
            next_product.previous = selected_product
            previous_product.save(reorder=False)
            next_product.save(reorder=False)
        elif previous_product.next == all_product[0]:
            #print("selected product is the last one")
            if previous_product.next == previous_product:
                # there's only one product in the database
                # this correct a bug, when two object save the same object one after the other
                # the second save will be discard
                next_product = previous_product
            else:
                next_product = previous_product.next
            selected_product.next = next_product
            selected_product.previous = previous_product
            previous_product.next = selected_product
            next_product.previous = selected_product
            next_product.save(reorder=False)
            previous_product.save(reorder=False)
        else:
            #print("selected product is somewhere in the middle")
            selected_product.previous = previous_product
            selected_product.next = previous_product.next
            previous_product.next = selected_product
            selected_product.next.previous = selected_product
            previous_product.save(reorder=False)
            selected_product.next.save(reorder=False)


    def remove_product_position(self, selected_product):
        #print("remove_product_position is getting called")
        #import time
        #print("removing product = %s " % selected_product)
        #print("removing product.id = %s " % selected_product.id)
       
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

    def set_previous_next_product(self, selected_product, previous_product, next_product):
        products = self.all()
        for product in products:
            if product.next == selected_product:
                #print("found next product : %s->%s " % (product, product.next))
                product.next = selected_product.next
                product.save(reorder=False)
            if product.previous == selected_product:
                #print("found previous product : %s<-%s " % (product.previous, product))
                product.previous = selected_product.previous
                product.save(reorder=False)

        
        #if previous_product != None:
            #previous_product.save()
        #if next_product != None:
            #next_product.save()
        
            