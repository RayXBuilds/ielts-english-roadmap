items=[]
def add(w,k,title,prompt,model,plan,feedback,errors,rewrite,data=''):
 items.append(dict(week=w,kind=k,title=title,prompt=prompt,model=model,plan=plan,feedback=feedback,errors=errors,rewrite=rewrite,data=data))
add(21,'T1A','晚间课程报名趋势','The graph shows enrolments in three types of evening course at a learning centre in selected years between 2012 and 2024. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.',
'''The graph compares enrolments in language, computing and cookery courses at a learning centre in four selected years from 2012 to 2024. The figures represent course enrolments rather than necessarily different individuals.

Overall, language courses attracted the most enrolments in the first three years shown, but computing became the largest category in 2024. Computing enrolments increased throughout, whereas language enrolments rose initially and then declined. Cookery remained the smallest category despite an increase over the period.

In 2012, languages recorded 300 enrolments, compared with 150 for computing and 100 for cookery. By 2016, the language figure had reached its peak of 360, while computing rose to 240 and cookery to 140. Languages therefore retained a substantial lead at that point.

In 2020, language enrolments fell to 330 and computing increased to 300, reducing the gap to just thirty. Cookery remained unchanged at 140. In the final year, computing reached 390 enrolments, ninety more than languages, which returned to 300. Cookery rose to 170. Consequently, the three categories together accounted for 860 enrolments in 2024, compared with 550 in 2012.''',
'首答20分钟内完成概述和主比较；读清报名次数非独立人数；查首尾、峰值与持平，最后核拼写和单位。',
['P1 enrolments不等于独立学生，同人可能报多课。','P2 computing末年领先，cookery一直最小；languages不是持续上涨。','P3 2016语言峰360，另两类240/140；不补收费或宣传原因。','P4 2020差30、2024差90；厨艺2016/2020持平140；合计550→860，算术可回查。'],
'把报名当不同人数；漏持平；只检查单词不查概述或单位。',
'完整重写至少150词；如存在漏项/拼写疑点才修正，保留原词与依据；如无则记录核查通过。按所选纸笔或键入方式限时，但不能据此声称实际考场界面练习完成。',
'![Evening-course enrolments](assets/figure.svg)\n\n教学虚构。2012/2016/2020/2024：Languages300/360/330/300，Computing150/240/300/390，Cookery100/140/140/170。单位报名次数，可一人多课；未给价格、人数或开课频率。')
add(21,'T1G','要求核对课程报名信息','''You booked a short course, but the confirmation contains incorrect information. Write to the course administrator. In your letter:
- give the details of the booking you intended to make
- describe the incorrect information in the confirmation
- ask for the corrections and confirmation you need.
Begin your letter: Dear Sir or Madam,''',
'''Dear Sir or Madam,

I am writing about my booking for the introductory gardening course, reference GD417. I intended to join the Saturday morning group beginning on 8 September. When I completed the booking form, I selected that group because I work during the week and can only attend at weekends.

The confirmation I received yesterday lists the Thursday evening group instead. It also spells my surname as Chan, although I entered Chen on the form. The email address and telephone number shown in the confirmation are correct. I would like to have the group and name checked before any course materials or attendance records are prepared.

Could you please transfer the booking to the Saturday group, if a place is still available, and correct the spelling of my name? I would appreciate a revised confirmation showing the starting date, session time and location. If the Saturday group is already full, please let me know what alternatives are available before changing my booking to another group. I have attached the original booking summary so that you can compare the details.

Yours faithfully,
Alex Chen''',
'正式核对；原拟报名与收到信息分开。示例选择姓名和组别两项差异，学生可合理自拟其他错误信息；备选未获同意不假定。',
['P1 编号/原选周六及原因完整，属于虚构书信情境非真实订单。','P2 周四组及Chan/Chen两误差明确；正确联系方式不误改。','P3 请求改正与新确认要点齐全；满员则先告知选项，不声称已转成功。'],
'漏自己设定的错误信息或更正请求；若采用本示例的姓名/组别设定，需前后一致，但题目不强制学生使用这两项具体错误。',
'整篇重写至少150词；核对三个题干要点、名字、日期和请求语气。如无错误记通过，不制造错字；实际所选输入方式单独登记。')
add(21,'T2','四天工作周','Some employers are considering a four-day working week with no reduction in weekly pay. Do the advantages of this arrangement outweigh the disadvantages? Give reasons and include relevant examples.',
'''A four-day working week without lower weekly pay could give employees more time outside work, but it also raises questions about workload and service coverage. I believe its advantages can outweigh its disadvantages in suitable workplaces, provided that employers redesign the work rather than simply compress five days of tasks into four exhausting days.

The main potential benefit is additional time for rest and personal responsibilities. An employee might use the extra day for appointments, family activities or learning without repeatedly interrupting the working week. This could make the job more attractive and help staff remain with an organisation. However, the benefit depends on whether the free day is genuinely protected. If unfinished tasks routinely spill into it, the apparent reduction in working days achieves much less.

The disadvantages are particularly clear where a service must remain available throughout the week. A customer support team, for example, cannot assume that customers will stop needing help on the fifth day. Covering the same opening hours may require staggered schedules or additional staff. Some employees could also face more intense working days, making the arrangement less comfortable than its name suggests. These costs should be included in any comparison rather than treated as minor implementation details.

In my view, a limited trial offers a better approach than either rejecting the idea or introducing it everywhere at once. A workplace could reduce unnecessary meetings, distribute coverage across different teams and monitor both employee workload and service quality. If the trial shows that tasks are being rushed or that staff work unofficially on the extra day off, the arrangement should be adjusted rather than declared successful merely because the schedule has changed.

Overall, the extra personal time can be a substantial advantage, but it is not created by a calendar change alone. The case is strongest where work can be reorganised without transferring unreasonable pressure to employees or customers.''',
'权衡限定适用工作场景，不把四天等于总工时自动减少；按休息、覆盖与强度比较，试点需证据。',
['P1 条件式利大，no reduction pay已回应，不讨论自愿减薪兼职。','P2 休息/责任便利有机制，真正休息日是条件。','P3 服务覆盖与强度成本具体，不假设所有岗位相同。','P4 试点看实际负担质量，不凭新日历宣布成功。','P5 和首段一致，没有保证生产率上涨。'],
'把四天必然等于轻松；忘服务需求；用虚构研究证明固定百分比效果。',
'完整重写至少250词；限时核主张、例子与限制。如发现长句或拼写问题才修；结束时标真实完成位置，不靠额外时间伪报按时完成。')
add(22,'T1A','二手织物分流流程','The diagram shows how donated textiles are sorted at a community reuse centre. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.',
'''The diagram illustrates how a community reuse centre sorts donated textiles. It begins with accepting donations and checking them, and ends with distribution for reuse, transfer for recycling or disposal.

Overall, the process separates items according to their condition and the work needed to make them usable. Some donations can be reused directly after sorting, while others are repaired first. Items unsuitable for reuse are checked for recycling eligibility rather than being automatically discarded.

Initially, donations are received and examined. Items that are already suitable for reuse move directly to a storage area. Those with repairable faults are sent for repair and then checked again. If the repair succeeds, these items join the usable donations in storage. The stored items are subsequently distributed through the centre’s reuse programme.

Donations that are unsuitable for repair, together with items that fail the check after repair, follow a separate route. Staff assess whether they meet the recycling requirements. Eligible textiles are sent to a recycler, whereas ineligible items are disposed of. The diagram does not show how the recycler processes the materials, nor does it give the time required for any stage.''',
'三终点与修复后复核；不把失败直接处置，先查回收资格；题面无频次/时间不能补daily。',
['P1 reuse/recycling/disposal三种结果，不增加销售或出口目的地。','P2 repair条件与recycling资格区分，概述有逻辑。','P3 直接可用入储存，修后通过才合流；无清洗步骤不能自加。','P4 不可修及修失败进入回收资格检查；eligibility不是全部可回收，不给工序时长。'],
'给范文自加daily/weekly；把修复失败直接丢弃；把送回收商当再生过程已知。',
'完整重写至少150词；如出现图外步骤、频次或时长则删去，清楚者保留。归档真实用时和覆盖，原创检查不能填正式T22完成。',
'![Textile sorting process](assets/figure.svg)\n\n教学虚构简化工作流：接收→检查。可直接再用→储存；可修→维修→复核，通过→储存，不通过→回收资格评估；不可修→回收资格评估。储存→再用项目分发。符合回收要求→送回收商；不符合→处置。未给频次、时长、清洗步骤、销售或回收商处理工艺。')
add(22,'T1G','联系慈善中心捐赠安排','''You would like to donate some household items to a community organisation. Write to the donations coordinator. In your letter:
- describe the items you would like to donate
- explain why you are offering them
- ask about the requirements and arrangements for donating them.
Begin your letter: Dear Sir or Madam,''',
'''Dear Sir or Madam,

I am writing to ask whether your organisation could accept some household items. I have a small wooden table, four matching chairs and two desk lamps that I no longer need. The furniture is in good condition apart from a few marks on the tabletop, and both lamps were working when I last used them.

I am moving to a furnished flat next month, so there will be no space for these items in my new home. I would prefer them to be used by someone else rather than simply left in storage. A neighbour mentioned your organisation’s work, which is why I am contacting you before making other arrangements.

Could you please explain which of these items you are able to accept and whether you need photographs or further information about their condition? I would also like to know whether you offer collection or whether donations must be delivered to your centre. If delivery is required, please tell me which days and times are suitable. I can make arrangements during the next two weekends, but I would like to confirm the requirements before moving anything.

Yours faithfully,
Alex Chen''',
'正式询问不是强制机构接收；物品情况、原因、资格/收送两类安排具体，未承诺安全认证。',
['P1 物品数量和状态限定为最后使用时，不声称已专业检验。','P2 搬家空间理由直接；不是自夸慈善历史。','P3 接受范围与需证据、收送时间都有请求，先确认再搬。'],
'假定机构必接收或免费上门；漏物品状态；将最后使用时工作正常当安全保证。',
'整篇重写至少150词；按题干核资格与安排问句，问题存在才改；保留真实初稿/重写区分，不把本课当正式T22评分。')
add(22,'T2','父母还是学校教生活技能','Some people think parents should teach children practical everyday skills, while others believe schools should take responsibility for this. Discuss both views and give your own opinion. Give reasons and include relevant examples.',
'''Practical skills such as organising belongings, preparing simple food and managing small tasks are useful in everyday life. Parents and schools can both help children acquire them. I believe the responsibility should be shared, with families providing regular opportunities to practise and schools ensuring that basic learning is not left entirely to differences between homes.

Parents are well placed to connect a skill with a real purpose. A child can help prepare a shopping list, for example, and then see how that list guides an actual trip. Practice can happen repeatedly in familiar surroundings, and an adult can adjust the task to the child’s current ability. However, this approach depends on time, confidence and suitable opportunities at home. It would be unrealistic to assume that every family can provide the same range of experiences.

Schools can offer a more consistent starting point. A lesson on organising a small group project could teach planning and cooperation to children who have had little chance to practise those skills elsewhere. Teachers can also explain a task in stages and observe how different pupils respond. Nevertheless, school time is limited, and a lesson cannot reproduce every situation children will meet outside the classroom. Adding practical activities without considering the existing timetable could reduce the time available for other important learning.

A shared approach would address these limitations better than assigning the whole responsibility to either side. Schools could introduce a small set of useful routines, while families could be given simple suggestions for practising them when circumstances allow. The aim should not be to judge parents whose resources differ, but to give children more than one route to learning. Progress should be assessed through what children can do, rather than through whether every household completes identical activities.

In conclusion, families offer meaningful everyday practice, while schools can provide wider and more consistent access. Cooperation between them is more likely to meet different children’s needs than a rule that makes only one side responsible.''',
'双方讨论并给共享责任；承认家庭差异与学校时数，实际学习目标而非责任互推。',
['P1 具体技能例与立场清楚，不声称所有家长或教师有同样能力。','P2 购物单联系真实任务并讲重复机会，家庭条件限制保留。','P3 学校提供共同起点，同时时间成本具体。','P4 介绍/家庭可选练习合作，不能将未做家庭作业作为道德指责。','P5 回扣两方优势，没有偷换成是否上大学。'],
'只赞父母关爱而无技能机制；忽略一方；宣称学校能完全替代家庭实践。',
'完整重写至少250词；如有单边或不回应的段落则调整，无问题记录通过证据；本题只记原创表现，正式目标与单项结果另列。')
add(23,'T1A','河岸步行区改造','The maps show a riverside area in 2010 and after changes in 2025. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.',
'''The maps compare a riverside area in 2010 and 2025. The river runs along the northern edge of both maps, while a road forms the southern boundary.

Overall, the area became more accessible for pedestrians and gained recreational facilities. A warehouse was replaced by a café and visitor centre, and the open ground in the east became a garden. The existing bridge and the road remained in place.

In 2010, the warehouse occupied the western part of the site, between the road and the river. By 2025, it had been replaced by a smaller café and visitor centre within the same general area. A footpath was added along the southern bank of the river, connecting the bridge on the western side with the eastern end of the site.

The eastern open ground was converted into a garden with a seating area. A new north-south pedestrian link connected this garden and the riverside footpath to the road. The bridge still crossed the river at the same position in the west, and no change was shown to the road’s alignment. Thus, the main alterations occurred within the area between these existing transport features.''',
'反馈核验需要图上证据；西仓库替换、东空地花园、新沿河路/南北链接与保留桥路；不推车流。',
['P1 北河、南路是基准；图未提供全城交通。','P2 accessible指新增步道联系，不假造无障碍认证。','P3 咖啡访客中心在原西部区域且更小，沿河南岸连接西桥与东端。','P4 花园和南北链接可指出；桥位与路走向不变，不能说新建桥。'],
'混淆南岸与北岸；把新步道写成车道；无图据接受AI关于拆桥建议。',
'完整重写至少150词；如反馈与图不符则标争议并求核实，不盲改；向第二轮真人评阅交原稿、图与改动依据，未有真人意见就记待安排。',
'![Riverside redevelopment](assets/figure.svg)\n\n教学虚构示意图，北向上不按比例。河沿北边、路沿南边，两年不变；西侧桥跨河位置不变。2010西部Warehouse、东部Open ground。2025西部以更小Café + visitor centre替换仓库，东部Garden + seating；新增河南岸东西Footpath，并新增东部南北Pedestrian link连接道路、花园与沿河步道。没有车流或实际坡度数据。')
add(23,'T1G','请求导师对修改稿反馈','''You have revised a report after receiving advice from your course tutor. Write to your tutor, Ms Carter. In your letter:
- explain which report you revised
- describe the changes you made
- ask for feedback on one aspect that you are still unsure about.
Begin your letter: Dear Ms Carter,''',
'''Dear Ms Carter,

I am writing about the short project report on the use of shared study spaces that I submitted last month. Thank you for suggesting that I make the purpose of each section clearer. I have now prepared a revised version and would appreciate your comments when you have time to look at it.

The introduction now states the question I investigated before describing the locations I visited. I have also moved the details about individual observations into a separate section, so that they no longer interrupt the comparison between the two spaces. In the conclusion, I have removed a general claim about all students and limited the discussion to the observations included in the report.

I am still unsure whether the comparison section explains the differences clearly enough. Could you comment on whether the examples support the main points, or whether I need to organise them differently? I have attached both versions and highlighted the changed passages to make the revision easier to follow. If a short meeting would be more convenient than written comments, I am available after class on Tuesday or Thursday.

Best wishes,
Alex Chen''',
'书信角色情境自带已收建议，非真实学生已经获批改；说明稿件/修订/一项待评焦点，半正式。',
['P1 定位报告与主题、请求时间礼貌；仅虚构信件角色经历。','P2 三项调整为原创例文自拟，学生可用其他合理修订，不强制照搬。','P3 聚焦comparison examples支持与组织，附版本便利评阅，时间可执行。'],
'将示例修订冒充自己真实课程已完成；问题泛成is it good；漏修改内容。',
'完整重写至少150词；按虚构角色合理自拟修改细节，不强制使用示例改法。真实第二轮反馈状态在证据表另记，没收意见不得填写已收。')
add(23,'T2','信息过载','Many people receive more information than they can use in their daily lives. What problems can this cause, and what could individuals and organisations do to address these problems? Give reasons and include relevant examples.',
'''Receiving a large amount of information can make it harder to identify what requires attention. The main problems are distraction and the possibility of missing important details among less useful messages. Individuals and organisations can reduce these difficulties by making priorities and communication purposes clearer.

One problem is the interruption of sustained work. A person may repeatedly stop a task to check messages that seem urgent but have little relevance to it. Even when each interruption is brief, returning to the original task can require effort. Another problem is uncertainty about what matters. If routine updates and genuinely important changes arrive in the same form, recipients may either spend too much time checking everything or overlook a message that requires action.

Individuals can respond by setting aside appropriate times to review non-urgent information and by reducing subscriptions or alerts they no longer use. This is not a recommendation to ignore all incoming messages. Some responsibilities require a prompt response, so the approach should reflect the person’s role. A useful first step is to distinguish information needed for an immediate decision from material that can be read later or not at all.

Organisations also have a responsibility to communicate selectively. A message should make clear who needs it, what action is required and when that action matters. Routine information could be gathered into a regular summary rather than sent as many separate interruptions. However, an urgent update should not be hidden in that summary simply for consistency. Clear channels and agreed expectations are more helpful than asking every employee to cope individually with an unlimited stream.

In conclusion, excess information can consume attention and obscure important messages. Personal filtering and more purposeful organisational communication would address both problems, provided that urgent and non-urgent needs are distinguished rather than treated identically.''',
'问题+两主体措施，不误写仅原因；干扰/漏重要内容分别展开；限时控制不提出无依据万能断网。',
['P1 两问题对应attention与important details。','P2 中断与优先级混淆分开，未编次数/时间损耗研究。','P3 个人按角色过滤，urgent例外防止不合理一刀切。','P4 组织收件人/行动/时间与汇总，紧急不藏汇总。','P5 回应题目，不偷换成技术全面有害。'],
'写互联网历史替代问题；只提个人不提组织；把所有消息都推迟。',
'完整重写至少250词；依据真实反馈优先修有证据问题，无真人意见先作自评并标待评；保留初稿和不同版本，第二轮意见不能被AI反馈替代。')
add(24,'T1A','学习中心模式构成与总参与量','The charts show the proportions of course enrolments in classroom, online and blended formats at a training provider in 2016 and 2026. The table gives total enrolments in each year. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.',
'''The charts compare the shares of enrolments in classroom, online and blended courses at a training provider in 2016 and 2026. The table gives the overall number of enrolments, allowing the quantities for individual formats to be calculated.

Overall, classroom courses lost share but remained the largest category in 2026. Both online and blended learning gained share, and total enrolments doubled. As a result, the number of classroom enrolments increased despite the decline in their proportion.

In 2016, classroom teaching accounted for 70% of the provider’s 2,000 enrolments, equivalent to 1,400. Online courses represented 20%, or 400 enrolments, while blended courses had the smallest share at 10%, corresponding to 200 enrolments.

By 2026, the total had risen to 4,000. Classroom courses made up 40%, giving 1,600 enrolments, while online courses accounted for 35%, or 1,400. The remaining 25%, equivalent to 1,000 enrolments, were in blended courses. The gap between classroom and online shares therefore narrowed from fifty to five percentage points. Blended enrolments increased fivefold in number, whereas their share rose by fifteen percentage points. The data describe enrolments rather than separate individual learners.''',
'比例与绝对量同时看；末年仍classroom40最大；参加人数未知，首尾核算用于证据不是成绩。',
['P1 2000/4000允许算各类数量，不能把enrolments当不同人。','P2 classroom比例70→40降，但件数1400→1600升。','P3 2016各1400/400/200，合2000。','P4 2026各1600/1400/1000合4000；gap50→5，blended数量5倍但份额+15点。'],
'比例降就说人数降；算5倍占比而非数量；将登记次数充正式学习效果。',
'完整重写至少150词；有证据问题才改，核对数量/比例/分母。保存真实作答记录供W24证据表，不以本题完成或示例推断报考准备度。',
'![Course format shares and totals](assets/figure.svg)\n\n教学虚构。2016总报名2000：Classroom70%、Online20%、Blended10%；2026总4000：40%、35%、25%。每份报名只归一种模式，各年合100%；同一人可多报，独立人数未知。Blended指同一课程结合线上与面授。')
add(24,'T1G','询问考试准备工作坊安排','''You are interested in a short preparation workshop advertised by a training centre. Write to the centre manager. In your letter:
- explain what you hope to practise
- ask about the activities and feedback provided
- ask for the practical information you need before deciding whether to attend.
Begin your letter: Dear Sir or Madam,''',
'''Dear Sir or Madam,

I saw your advertisement for a short preparation workshop and would like some further information before deciding whether to attend. I am particularly interested in practising timed writing and receiving specific comments on how clearly I respond to a task. I would also like an opportunity to practise answering spoken questions without reading from prepared notes.

Could you explain how the workshop sessions are organised? For example, will participants complete individual tasks during the session, or will most of the time be used for demonstrations? I would also like to know who provides the feedback and whether it refers to each participant’s own writing and speaking. A general explanation of useful techniques would be welcome, but individual comments are important to my decision.

Please send the dates, session length, group size and total fee, including any charge for reviewing work afterwards. I would also appreciate information about the equipment participants need to bring and whether a sample schedule is available. Once I understand the activities and practical arrangements, I will be able to judge whether the workshop fits my needs and availability.

Yours faithfully,
Alex Chen''',
'正式询问信，目标练习可自拟；问反馈谁提供/是否个人实际作业，费用设备日程未给就问不编。',
['P1 希望练习的内容明确，但不是用户已报名或已诊断的事实。','P2 individual tasks/demo、反馈者/个别反馈为问题，不能假装机构官方认证。','P3 日期时长人数总费设备和样表支持决策，不提前承诺参加。'],
'虚构已获分数或教师资历；把广告当保分承诺；只问价格忘训练与反馈。',
'整篇重写至少150词；学生可合理自拟希望练习的内容，不必采用示例的具体弱项。真实报名/报考判断另据证据表，不把这封虚构信当已发送或已报名。')
add(24,'T2','迁居城市工作利弊','Many adults move from smaller towns to large cities in search of work. Do the advantages of this development outweigh the disadvantages? Give reasons and include relevant examples.',
'''Moving to a large city can widen an adult’s employment options, but it can also bring higher living costs and a loss of familiar support. I believe the advantages can outweigh the disadvantages when the move is connected to realistic opportunities, although relocation should not be regarded as beneficial for everyone.

The main advantage is access to a wider range of employers and specialised roles. A person whose skills are needed by only a few organisations may have more opportunities where those organisations are concentrated. Changing jobs may also become easier without another major move. These benefits are particularly relevant when a smaller town offers little work in the person’s field. However, a larger number of vacancies does not guarantee that an individual will obtain a suitable position.

The disadvantages concern both money and daily life. Housing and travel can absorb much of the benefit from a higher salary, so comparing pay alone gives an incomplete picture. A person may also lose the practical help and social connections available near family or long-standing friends. Building a new support network takes time. For someone with responsibilities that depend on nearby relatives, this loss may be more significant than access to additional employers.

On balance, the case for moving is stronger when a person can compare a concrete opportunity with the actual costs and arrangements involved. Information about accommodation, commuting and the stability of the work is therefore important. There are also alternatives: some roles can be performed remotely, and some people may find suitable work in a regional centre rather than the largest city. These options do not eliminate the value of relocation, but they show why the decision should be based on circumstances rather than a simple assumption that bigger places are always better.

In conclusion, large cities can offer valuable employment advantages, especially for specialised work. Whether those gains exceed the disadvantages depends on the opportunity available and the effect of the move on the person’s overall living conditions.''',
'利弊条件式权衡，用具体机会与整体生活而非只比薪水；不是为真实用户职业/财务选择下结论。',
['P1 opportunities与cost/support两方明确，条件不空泛。','P2 专门岗位与雇主集中机制，机会不等于保证offer。','P3 住房交通与支持网络多维成本，不能只算收入。','P4 actual opportunity/cost与remote/regional替代作范围限制，不否认所有城市收益。','P5 判断与开头一致，不自动建议任何人搬家。'],
'把所有大城市写成高薪低风险；忽略support；只有利弊列表没有判断依据。',
'完整重写至少250词；根据本次及真实历史稿核是否有重复问题，无证据保持未知。保存真实限时稿供独立评阅，报考/延长不能由范文字数或本包完结决定。')
