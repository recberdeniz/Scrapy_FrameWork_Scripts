# names = response.css("div.col.search_name.ellipsis span.title::text").extract()
# published_date = response.css("div.col.search_released.responsive_secondrow::text").extract()
# for i in response.css("div.col.search_discount.responsive_secondrow"):
#      if i.css("span::text"):
#           newDiscount.append(i.css("span::text").extract_first())
#      else:
#           newDiscount.append("")
# review_score = response.css("span.search_review_summary::attr(data-tooltip-html)").extract()
#for i in response.css("div.col.search_reviewscore.responsive_secondrow"):
#     if i.css("span.search_review_summary::attr(data-tooltip-html)"):
#         review_score.append(i.css("span.search_review_summary::attr(data-tooltip-html)").extract_first())
#     else:
#         review_score.append("")
#
#
#prices = response.css("div.col.search_price_discount_combined.responsive_secondrow::attr(data-price-final)").extract()