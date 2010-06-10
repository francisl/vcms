/* ************************************************************************

   Copyright:

   License:

   Authors:

************************************************************************ */

/* ************************************************************************

#asset(vcms/client/*)

************************************************************************ */

/**
 * This is the main application class of your custom application "vcms.client"
 */
qx.Class.define("vcms.client.Application",
{
  extend : qx.application.Standalone,



  /*
  *****************************************************************************
     MEMBERS
  *****************************************************************************
  */

  members :
  {
    /**
     * This method contains the initial application code and gets called 
     * during startup of the application
     * 
     * @lint ignoreDeprecated(alert)
     */
    main : function()
    {
      // Call super class
      this.base(arguments);

      // Enable logging in debug variant
      if (qx.core.Variant.isSet("qx.debug", "on"))
      {
        // support native logging capabilities, e.g. Firebug for Firefox
        qx.log.appender.Native;
        // support additional cross-browser console. Press F7 to toggle visibility
        qx.log.appender.Console;
      }

      /*
      -------------------------------------------------------------------------
        Below is your actual application code...
      -------------------------------------------------------------------------
      */
      
      var doc = this.getRoot();
      
      var main_container = new qx.ui.container.Composite(new qx.ui.layout.HBox().set({ spacing: 10 }));
      doc.add(main_container);
      
      // Left container
      var left_container = new qx.ui.container.Composite(new qx.ui.layout.VBox().set({ spacing: 2 })).set({ width: 300 });
      main_container.add(left_container);
      var tree = new qx.ui.tree.Tree().set({
        width: 600,
        height: 500
      });
      left_container.add(tree);
      var root = this.configureTreeItem(new qx.ui.tree.TreeFolder(), "Root");
      tree.setRoot(root);
      tree.setHideRoot(true);
      root.setOpen(true);
      // Gets the list of available pages
      var req = new qx.io.remote.Request("/ajax/page/list/", "GET", "application/json");
      req.addListener("completed", function(e)
      {
        // TODO
        var te1 = this.configureTreeItem(new qx.ui.tree.TreeFolder(), "Desktop");
        root.add(te1);
      }, this);
      req.send();
      var buttons_left_container = new qx.ui.container.Composite(new qx.ui.layout.HBox().set({ spacing: 5 }));
      left_container.add(buttons_left_container);
      buttons_left_container.add(new qx.ui.form.Button("Add a simple page"));
      buttons_left_container.add(new qx.ui.form.Button("Add a main page"));
      buttons_left_container.add(new qx.ui.form.Button("Add a news page"));
      
      // Center container
      var center_container = new qx.ui.container.Composite(new qx.ui.layout.VBox()).set({ width: 400 });
      var tabs_center_container = new qx.ui.tabview.TabView();
      for (i = 0, n = 3; i < n; i++)
      {
        var page = new qx.ui.tabview.Page("Page #" + i);
        tabs_center_container.add(page);
        page.setLayout(new qx.ui.layout.VBox().set({ spacing: 2 }));
        page.add(new qx.ui.form.List());
        page.add(new qx.ui.form.Button("Remove widget from page"));
      }
      center_container.add(tabs_center_container);
      main_container.add(center_container);
      
      // Right container
      var right_container = new qx.ui.container.Composite(new qx.ui.layout.VBox().set({ spacing: 2 })).set({ width: 150 });
      main_container.add(right_container);
      right_container.add(new qx.ui.form.List());
      right_container.add(new qx.ui.form.Button("Add widget to page"));
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
  }
});