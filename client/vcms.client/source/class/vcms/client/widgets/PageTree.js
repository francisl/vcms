qx.Class.define("vcms.client.widgets.PageTree",
{
    extend : qx.ui.tree.Tree,
 
    construct : function()
    {
        this.base(arguments);
        
        var root = this.configureTreeItem(new qx.ui.tree.TreeFolder(), "Root");
        this.setRoot(root);
//        this.setHideRoot(true);
        root.setOpen(true);
        // Gets the list of available pages
//        var controller = new qx.data.controller.Tree(null, tree, "pages", "menu_name");
        var store = new qx.data.store.Json("/ajax/page/list/");
//        alert(store.getModel());
//        var json = qx.util.Json.parse(store.getModel());
//        alert(qx.util.Json.parse.stringify(json));
//        store.bind("model", controller, "model");
//        store.bind("state", status, "value");
//        store.addListener("loaded", function(ev) {
//          tree.getRoot().setOpen(true);
//        }, this);
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

