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
            var buttons_container = new qx.ui.container.Composite(new qx.ui.layout.HBox());
            page.add(buttons_container);
            buttons_container.add(new qx.ui.form.Button("Remove widget from page"), {flex: 0});
            buttons_container.add(new qx.ui.core.Spacer(), {flex: 1});
            this.add(page);
        }
    }
});

