<%
' Database connection function
Function GetConnection()
    Dim conn
    Set conn = Server.CreateObject("ADODB.Connection")
    conn.Open "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" & Server.MapPath("/db/fakestore.mdb")
    Set GetConnection = conn
End Function
%>
