from django.test import TestCase

from admin_tabs.helpers import TabbedPageConfig, Config

__all__ = ["TabsConfigsInheritanceTests", "TabsConfigOrderTests"]

class TabsConfigsInheritanceTests(TestCase):

    def test_should_inherit_from_parent(self):
        """
        When a PageConfig inherit from another, it must inherit the tabs of its
        parent.
        """

        class A(TabbedPageConfig):
            
            class TabsConfig:
                a_tab = Config(name='a_tab')
        
        class AB(A):
            
            class TabsConfig:
                b_tab = Config(name="b_tab")

        class AD(A):
            
            class TabsConfig:
                d_tab = Config(name="d_tab")

        class ABC(AB):
            
            class TabsConfig:
                c_tab = Config(name="c_tab")

        # A must have only its attribute
        self.failUnless(hasattr(A.TabsConfig, "a_tab"))
        self.assertEqual(A.TabsConfig.a_tab["name"], "a_tab")
        self.failIf(hasattr(A.TabsConfig, "b_tab"))

        # AB must have its attribute and A's one
        self.failUnless(hasattr(AB.TabsConfig, "b_tab"))
        self.failUnless(hasattr(AB.TabsConfig, "a_tab"))
        self.assertEqual(AB.TabsConfig.a_tab["name"], "a_tab")
        self.assertEqual(AB.TabsConfig.b_tab["name"], "b_tab")
        self.failIf(hasattr(AB.TabsConfig, "c_tab"))
        self.failIf(hasattr(AB.TabsConfig, "d_tab"))

        # ABC must have its attribute, AB's one and A's one
        self.failUnless(hasattr(ABC.TabsConfig, "c_tab"))
        self.failUnless(hasattr(ABC.TabsConfig, "b_tab"))
        self.failUnless(hasattr(ABC.TabsConfig, "a_tab"))
        self.assertEqual(ABC.TabsConfig.a_tab["name"], "a_tab")
        self.assertEqual(ABC.TabsConfig.b_tab["name"], "b_tab")
        self.assertEqual(ABC.TabsConfig.c_tab["name"], "c_tab")
        self.failIf(hasattr(ABC.TabsConfig, "d_tab"))


class TabsConfigOrderTests(TestCase):
    
    def test_should_keep_natural_order(self):
        """
        With no order asked, the order must be the order of the tabs in the
        python file.
        """

        class A(TabbedPageConfig):
            
            class TabsConfig:
                # We suffix names with integers to check that the final order 
                # will not be alphanumeric
                tab42 = Config(name='first')
                tab18 = Config(name='second')
                tab37 = Config(name='third')
                
        self.assertEqual(A.TabsConfig.tabs_order, ["tab42", "tab18", "tab37"])

    def test_user_defined_tabs_order_should_have_priority(self):

        class A(TabbedPageConfig):
            
            class TabsConfig:
                tabs_order = ["tab1", "tab2", "tab3"]
                tab2 = Config(name='second')
                tab1 = Config(name='first')
                tab3 = Config(name='third')
                
        self.assertEqual(A.TabsConfig.tabs_order, ["tab1", "tab2", "tab3"])        
