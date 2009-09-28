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
        
        print("----------------------------------------")
        print("Selected product = %s " % selected_product)
        for product in all_product:
            print("product slug is ! %s" % product.slug)
            print("selected product slug is ! %s" % selected_product.slug)
            if product.slug == selected_product.slug:
                #selected_product.previous_product = previous_product
                print("product slug is selected product! %s, %s" % (product.slug, selected_product.slug))
                #product_is_set = True
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
        
        print("previous_product before condition : %s" % previous_product)
        if len(all_product) <= 1:
            print("Product is lonely")
            next_product = selected_product.next = selected_product
            previous_product = selected_product.previous = selected_product
        elif previous_product == selected_product:
            print("Product is the first one of many")
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
            print("selected product is the last one")
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
            
            print("previous_product.next after beiing saved = %s" % previous_product.next)
        else:
            print("selected product is somewhere in the middle")
            selected_product.previous = previous_product
            selected_product.next = previous_product.next
            previous_product.next = selected_product
            selected_product.next.previous = selected_product
            previous_product.save(reorder=False)
            selected_product.next.save(reorder=False)


    def remove_product_position(self, selected_product):
        print("remove_product_position is getting called")
        previous_product = selected_product.previous
        next_product = selected_product.next
        
        if previous_product == next_product:
            """ in condition there is only one product """
            previous_product.next = selected_product.next
            previous_product.previous = selected_product.previous
            previous_product.save(reorder=False)
        else:
            previous_product.next = selected_product.next
            next_product.previous = selected_product.previous
            previous_product.save(reorder=False)
            next_product.save(reorder=False)
            
        selected_product.previous = selected_product
        selected_product.next = selected_product
        selected_product.save(reorder=False)

