qx.Class.define("vcms.client.widgets.PageTree",
{
    extend : qx.ui.tree.Tree,
 
    construct : function()
    {
        this.base(arguments);
        
        var root = this.configureTreeItem(new qx.ui.tree.TreeFolder(), "root");
        this.setRoot(root);
        // Gets the list of available pages
        var controller = new qx.data.controller.Tree(null, this, "pages", "name");
        var store = new qx.data.store.Json("/ajax/page/list/");
        store.bind("model", controller, "model");
        store.addListener("loaded", function(e) {
          this.getRoot().setOpen(true);
        }, this);
    },
    members :
    {
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
    }
});

