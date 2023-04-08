
function init() {
    pxmu.loading({
        msg: '正在加载', //loading信息 为空时不显示文本
        time: 2500, //停留时间 
        bg: 'rgba(0, 0, 0, 0.65)', //背景色
        color: '#fff', //文字颜色
        animation: 'fade', //动画名 详见动画文档
        close: false, // 自动关闭 为false时可在业务完成后调用 pxmu.closeload();手动关闭
        inscroll: true, //模态 不可点击和滚动
        inscrollbg: 'rgba(0, 0, 0, 0.45)', //自定义遮罩层颜色 为空不显示遮罩层
    })
    $.ajax({
        url: `/getclasses?week=-1`,
        dataType: "json",
        type: "get",
        async: false,
        success: function (d) {
            d = d.list
            html = '<option value="" >全班级</option>'
            d.forEach(element => {
                html += `<option value="${element.id}">${element.name}</option>`
            });
            if (html == '') {
                html = '<option value="" >无班级</option>'
            }
            $('#search').html(html)
            $('#search').val(cid)
        },
        error: function (err) {
            pxmu.toast('加载失败')
        }
    })
    $.ajax({
        url: `/getteacher?week=-1`,
        dataType: "json",
        type: "get",
        async: false,
        success: function (d) {
            d = d.list
            html = '<option value="" >不限</option>'
            d.forEach(element => {
                html += `<option value="${element.id}">${element.name}</option>`
            });
            if (html == '') {
                html = '<option value="" >无教师</option>'
            }
            $('#search2').html(html)
            $('#search2').val(ctid)
        },
        error: function (err) {
            pxmu.toast('加载失败')
        }
    })
    $.ajax({
        url: `/getdata?week=${week}&cid=${cid}&tid=${tid}`,
        dataType: "json",
        type: "get",
        async: false,
        success: function (d) {
            week = d.week
            $('#week').text(week)
            d = d.list
            datas = document.querySelectorAll('.datas>div')
            for (var i = 0; i < 7; i++) {
                html = ''
                for (var j = 0; j < 6; j++) {
                    courses = ''

                    data = d[i][j]
                    data.forEach(e => {
                        courses += `
                        <div class="course" data-bs-toggle="modal" data-bs-target="#exampleModal" data-id='${e.id}' data-week='${e.week}' data-day="${e.day}" data-Section='${e.Section}' data-tid='${e.t_id}' data-rid='${e.r_id}' data-cid='${e.c_id}' data-subject='${e.subject}' data-teacher='${e.teacher}' data-room='${e.room}' data-class='${e.class}'>
                            <div>${e.subject}</div>@<span>${e.teacher}</span>@<i>${e.room}</i>@<strong>${e.class}</strong>
                        </div>
                        `
                    });
                    html += `
                    <div class="data">
                        <div id="course">
                            ${courses}
                        </div>
                     
                        <div class="fun" >
                                <i class="fa-solid fa-circle-plus add" data-bs-toggle="modal" data-bs-target="#addModal" data-week='${week}' data-day=${i+1} data-Section=${j+1}> </i>
                        </div>
                    </div>
                    `
                }
                datas[i].innerHTML = html
            }
            pxmu.closeload();
        },
        error: function (err) {
            pxmu.closeload();
            pxmu.toast('加载失败')
        }
    })

}
init()
function getselect(el,week,day,Section,type=''){
    pxmu.loading({
        msg: '正在加载', //loading信息 为空时不显示文本
        time: 2500, //停留时间 
        bg: 'rgba(0, 0, 0, 0.65)', //背景色
        color: '#fff', //文字颜色
        animation: 'fade', //动画名 详见动画文档
        close: false, // 自动关闭 为false时可在业务完成后调用 pxmu.closeload();手动关闭
        inscroll: true, //模态 不可点击和滚动
        inscrollbg: 'rgba(0, 0, 0, 0.45)', //自定义遮罩层颜色 为空不显示遮罩层
    })
    $.ajax({
        url: `/getteacher?week=${week}&day=${day}&Section=${Section}`,
        dataType: "json",
        type: "get",
        async: false,
        success: function (d) {

            d = d.list
            html = ''
            d.forEach(element => {
                html += `<option value="${element.id}">${element.name}</option>`
            });
            if(type=='' && html==''){
                html = `<option value="${el.getAttribute('data-tid')}" >${el.getAttribute('data-teacher')}</option>`
            }
            if (html == '') {
                html = '<option value="" >该时段无空闲老师</option>'
            }
            $('#teacherlist'+type).html(html)
        },
        error: function (err) {
            pxmu.closeload();
            pxmu.toast('加载失败')
        }
    })
    $.ajax({
        url: `/getroom?week=${week}&day=${day}&Section=${Section}`,
        dataType: "json",
        type: "get",
        async: false,
        success: function (d) {
            d = d.list
            html = ''
            d.forEach(element => {
                html += `<option value="${element.id}">${element.name}</option>`
            });
            if(type=='' && html==''){
                html = `<option value="${el.getAttribute('data-rid')}" >${el.getAttribute('data-room')}</option>`
            }
            if (html == '') {
                html = '<option value="" >该时段无空闲教室</option>'
            }
            $('#roomlist'+type).html(html)
        },
        error: function (err) {
            pxmu.closeload();
            pxmu.toast('加载失败')
        }
    })
    $.ajax({
        url: `/getclasses?week=${week}&day=${day}&Section=${Section}`,
        dataType: "json",
        type: "get",
        async: false,
        success: function (d) {
            d = d.list
            html = ''

            d.forEach(element => {
                html += `<option value="${element.id}">${element.name}</option>`
            });
            if(type=='' && html==''){
                html = `<option value="${el.getAttribute('data-cid')}" >${el.getAttribute('data-class')}</option>`
            }
            if (html == '') {
                html = '<option value="" >该时段无空闲班级</option>'
            }
            
            $('#classlist'+type).html(html)
            pxmu.closeload();
        },
        error: function (err) {
            pxmu.closeload();
            pxmu.toast('加载失败')
        }
    })
}
function initfrom() {
    document.querySelectorAll('.course').forEach(el => {

        el.addEventListener('click', function () {
            week = el.getAttribute('data-week')
            day = el.getAttribute('data-day')
            Section = el.getAttribute('data-Section')

            getselect(el,week,day,Section)
            $('#dataid').val(el.getAttribute('data-id'))
            $('#dataweek').val(week)
            $('#dataday').val(day)
            $('#dataSection').val(Section)
            $('#datasubject').val(el.getAttribute('data-subject'))
            $('#teacherlist').val(el.getAttribute('data-tid'))
            $('#classlist').val(el.getAttribute('data-cid'))
            $('#roomlist').val(el.getAttribute('data-rid'))
        })

    })
    document.querySelectorAll('.fun>i').forEach(el => {

        el.addEventListener('click', function () {
            week = el.getAttribute('data-week')
            day = el.getAttribute('data-day')
            Section = el.getAttribute('data-Section')
            getselect(el,week,day,Section,'2')
            $('#dataweek2').val(week)
            $('#dataday2').val(day)
            $('#dataSection2').val(Section)
        })

    })


}
initfrom()
function submitdata(){

    $('#del').click(function(){
        pxmu.loading({
            msg: '正在加载', //loading信息 为空时不显示文本
            time: 2500, //停留时间 
            bg: 'rgba(0, 0, 0, 0.65)', //背景色
            color: '#fff', //文字颜色
            animation: 'fade', //动画名 详见动画文档
            close: false, // 自动关闭 为false时可在业务完成后调用 pxmu.closeload();手动关闭
            inscroll: true, //模态 不可点击和滚动
            inscrollbg: 'rgba(0, 0, 0, 0.45)', //自定义遮罩层颜色 为空不显示遮罩层
        })
        id=$('#dataid').val()
        $.ajax({
        url: `/deldata?id=${id}`,
        dataType: "json",
        type: "get",
        success: function (d) {
            init()
            $('#close1').click()
            pxmu.closeload();
            pxmu.toast('删除成功')
            
        },
        error: function (err) {
            pxmu.closeload();
            pxmu.toast('删除失败')
            console.log(err)
        }
    })})

    $('#sub2').click(function(){
        pxmu.loading({
            msg: '正在加载', //loading信息 为空时不显示文本
            time: 2500, //停留时间 
            bg: 'rgba(0, 0, 0, 0.65)', //背景色
            color: '#fff', //文字颜色
            animation: 'fade', //动画名 详见动画文档
            close: false, // 自动关闭 为false时可在业务完成后调用 pxmu.closeload();手动关闭
            inscroll: true, //模态 不可点击和滚动
            inscrollbg: 'rgba(0, 0, 0, 0.45)', //自定义遮罩层颜色 为空不显示遮罩层
        })

        week=$('#dataweek2').val()
        day=$('#dataday2').val()
        Section=$('#dataSection2').val()
        subject=$('#datasubject2').val()
        teacher=$('#teacherlist2').val()
        Class=$('#classlist2').val()
        room=$('#roomlist2').val()

        $.ajax({
            url: `/adddata?week=${week}&day=${day}&Section=${Section}&subject=${subject}&t_id=${teacher}&r_id=${room}&c_id=${Class}`,
            dataType: "json",
            type: "get",
            success: function (d) {
                init()
                $('#close2').click()
                pxmu.closeload();
                pxmu.toast('添加成功')
            },
            error: function (err) {
                pxmu.closeload();
                pxmu.toast('添加失败')
                console.log(err)
            }
        })
    })



    $('#sub1').click(function(){
        pxmu.loading({
            msg: '正在加载', //loading信息 为空时不显示文本
            time: 2500, //停留时间 
            bg: 'rgba(0, 0, 0, 0.65)', //背景色
            color: '#fff', //文字颜色
            animation: 'fade', //动画名 详见动画文档
            close: false, // 自动关闭 为false时可在业务完成后调用 pxmu.closeload();手动关闭
            inscroll: true, //模态 不可点击和滚动
            inscrollbg: 'rgba(0, 0, 0, 0.45)', //自定义遮罩层颜色 为空不显示遮罩层
        })
        id=$('#dataid').val()
        week=$('#dataweek').val()
        day=$('#dataday').val()
        Section=$('#dataSection').val()
        subject=$('#datasubject').val()
        teacher=$('#teacherlist').val()
        Class=$('#classlist').val()
        room=$('#roomlist').val()

        $.ajax({
            url: `/adddata?id=${id}&week=${week}&day=${day}&Section=${Section}&subject=${subject}&t_id=${teacher}&r_id=${room}&c_id=${Class}`,
            dataType: "json",
            type: "get",
            success: function (d) {
                init()
                $('#close1').click()
                pxmu.closeload();
                pxmu.toast('修改成功')
            },
            error: function (err) {
                pxmu.closeload();
                pxmu.toast('修改失败')
                console.log(err)
            }
        })
    })
}
submitdata()