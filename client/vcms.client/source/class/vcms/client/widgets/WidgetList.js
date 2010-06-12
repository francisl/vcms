qx.Class.define("vcms.client.widgets.WidgetList",
{
    extend : qx.ui.tabview.TabView,
 
    construct : function()
    {
        this.base(arguments);
        
        for (i = 0, n = 3; i < n; i++)
        {
            var page = new qx.ui.tabview.Page("Page #" + i);
            page.setLayout(new qx.ui.layout.VBox().set({ spacing: 2 }));
            page.add(new qx.ui.form.List());
            page.add(new qx.ui.form.Button("Remove widget from page"));
            this.add(page);
        }
    }
});

