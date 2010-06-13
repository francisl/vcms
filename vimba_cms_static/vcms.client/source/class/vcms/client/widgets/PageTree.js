qx.Class.define("vcms.client.widgets.PageTree",
{
    extend : qx.ui.tree.Tree,
 
    construct : function()
    {
        this.base(arguments);
        
        var root = this.configureTreeItem(new qx.ui.tree.TreeFolder(), "root");
        this.setRoot(root);
        
        // Hide the root until the tree gets databound
        this.setHideRoot(true);
        
        // Get the list of available pages and databind them to the tree
        this.fillTree(this);
    },
    members :
    {
        fillTree : function(tree)
        {
            // Databind the tree with the JSON data
            var controller = new qx.data.controller.Tree(null, tree, "pages", "name");
            var store = new qx.data.store.Json(vcms.client.widgets.PageTree.JSON_PAGES_URL);
            store.bind("model", controller, "model");
            
            // Show the root and open it after the tree gets databound
            store.addListener("loaded", function(e) {
                this.setHideRoot(false);
                tree.getRoot().setOpen(true);
            }, this);
        },
        configureTreeItem : function(treeitem, label)
        {
          if (treeitem instanceof qx.ui.tree.TreeFolder)
            treeitem.addOpenButton();

          var checkbox = new qx.ui.form.CheckBox();
          checkbox.setFocusable(false);
          treeitem.addWidget(checkbox);

          treeitem.addLabel(label);

          treeitem.addWidget(new qx.ui.core.Spacer(), {flex: 1});

          return treeitem;
        }
    },
    statics :
    {
        JSON_PAGES_URL : "/ajax/page/list/"
    }
});

