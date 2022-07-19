//http://www.switchonthecode.com/tutorials/javascript-tutorial-how-to-auto-ellipse-text

function autoEllipseText(element, text, width)
{
    element.innerHTML = '<span id="ellipsisSpan" style="white-space:nowrap;">' + text + '</span>';
    inSpan = document.getElementById('ellipsisSpan');
    if(inSpan.offsetWidth > width)
    {
        var i = 1;
        inSpan.innerHTML = '';
        while(inSpan.offsetWidth < (width) && i < text.length)
        {
            inSpan.innerHTML = text.substr(0,i) + '...';
            i++;
        }

        returnText = inSpan.innerHTML;
        element.innerHTML = '';
        return returnText;
    }
    return text;
}