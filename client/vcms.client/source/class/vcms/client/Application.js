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
      for (i = 0, n = 15; i < n; i++)
          left_container.add(new qx.ui.form.Button("Button #" + i));
      var buttons_left_container = new qx.ui.container.Composite(new qx.ui.layout.HBox().set({ spacing: 5 }));
      left_container.add(buttons_left_container);
      buttons_left_container.add(new qx.ui.form.Button("Add a simple page"));
      buttons_left_container.add(new qx.ui.form.Button("Add a main page"));
      buttons_left_container.add(new qx.ui.form.Button("Add a news page"));
      
      // Center container
      var center_container = new qx.ui.container.Composite(new qx.ui.layout.VBox().set({ spacing: 2 })).set({ width: 400 });
      main_container.add(center_container);
      center_container.add(new qx.ui.form.List());
      center_container.add(new qx.ui.form.Button("Remove widget from page"));
      
      // Right container
      var right_container = new qx.ui.container.Composite(new qx.ui.layout.VBox().set({ spacing: 2 })).set({ width: 150 });
      main_container.add(right_container);
      right_container.add(new qx.ui.form.List());
      right_container.add(new qx.ui.form.Button("Add widget to page"));
    },
    members :
    {
      
    }
  }
});
